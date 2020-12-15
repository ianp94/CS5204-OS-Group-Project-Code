from sklearn.naive_bayes import GaussianNB
import json
from utils import list_files
from config import LogKeys, Config
import numpy as np
import logging
import fire
from sklearn.naive_bayes import CategoricalNB

# logging.basicConfig(filename='test.log', level=logging.INFO)

class Classifier():
    def __init__(self, log_keys, func2ids, existing_records_path=None):
        """
        A initial training to get a Naive Bayes model if there is some existing records to train
        :param existing_records_path:
        """
        super(Classifier, self).__init__()

        self.log_keys = log_keys
        self.gnb = GaussianNB()
        self.record = {}
        self.trained_recordID = {}
        self.is_newID = set()
        self.func2ids = func2ids

        if existing_records_path:
            self.read_log(existing_records_path)
            trainingX, trainingY = self.preprocessing()
            priorX = np.asarray(list(set(self.func2ids.values()) - set([x[0] for x in trainingX])))
            priorY = self.func2ids[self.log_keys.unknown] * np.ones_like(priorX)
            trainingX = np.concatenate((priorX.reshape(-1, 1), trainingX))
            trainingY = np.concatenate((priorY, trainingY))
            self.gnb.fit(trainingX, trainingY)

    def read_log(self, path):
        """
        Read log files from the path
        :param path:
        :return:
        """
        try:
            files = list_files(path)
        except (RuntimeError, TypeError, NameError) as err:
            logging.info("Error in listing files from path {}".format(path, err))
        files = [''.join([path, f]) for f in files]

        self.is_newID = set()

        for f in files:
            self.read_each_logs(f)
        return 0

    def read_each_logs(self, file):
        """
        Load json object from the file
        :param file:
        :return:
        """
        with open(file) as f:
            try:
                data = json.load(f)
            except:
                data = []
                print(f)
        for d in data:
            if self.log_keys.id in d.keys():
                this_id = d[self.log_keys.id]
            elif self.log_keys.id in d['doc'].keys():
                this_id = d['doc'][self.log_keys.id]
            else:
                this_id = 'unknown'
            if this_id not in self.trained_recordID:
                if 'doc' in d.keys():
                    self.record[this_id] = d['doc']
                else:
                    self.record[this_id] = d
                self.is_newID.add(this_id)
        return 0


    def preprocessing(self):
        """
        Preprocess records with recordID stored in self.is_newID
        :return:
        """
        trainingX, trainingY = [],[]
        for x in self.is_newID:
            if self.log_keys.causeID not in self.record[x].keys():
                causeID = 'unknown'
            else:
                causeID = self.record[x][self.log_keys.causeID]

            this_call = self.record[x][self.log_keys.name]
            try:
                cause_call = self.record[causeID][self.log_keys.name]
            except:
                cause_call = self.log_keys.unknown

            if this_call not in self.func2ids:
                self.func2ids[this_call] = len(self.func2ids.keys())
            if cause_call not in self.func2ids:
                self.func2ids[this_call] = len(self.func2ids.keys())
            this_call, cause_call = self.func2ids[this_call], self.func2ids[cause_call]
            trainingX.append(cause_call)
            trainingY.append(this_call)
        return np.asarray(trainingX).reshape(-1, 1), np.asarray(trainingY)

    def online_updates(self, new_branches, actual_next_branches):
        """
        Online updates with the new branch and its actual successive branch
        :param new_branches:
        :param actual_next_branches:
        :return:
        """
        self.gnb.partial_fit(new_branches, actual_next_branches)
        return 0

    def naive_bayes_prediction(self, new_branch):
        """
        Predict the next branch to initiate based on previous data and the current branch
        :param old_NB_model:
        :param new_branch:
        :return:
        """
        next_branch_to_initiate = self.gnb.predict(new_branch)
        return next_branch_to_initiate


def main(**kwargs):
    logKeys = LogKeys()
    config = Config()
    config.update(**kwargs)
    classifier = Classifier(logKeys, config.func2ids, config.logging_path)

    classifier.read_log(config.logging_path)
    trainingX, trainingY = classifier.preprocessing()
    classifier.online_updates(trainingX, trainingY)

    predict_dic = {}
    for func in classifier.func2ids:
        ids2func = dict((v, k) for k, v in classifier.func2ids.items())

        pred_id = classifier.gnb.predict([[classifier.func2ids[func]]])[0]
        prob = classifier.gnb.predict_proba([[classifier.func2ids[func]]])[0][pred_id]
        pred = ids2func[pred_id]
        predict_dic[func] = [pred, prob]

    return json.dumps(predict_dic, indent=4)

if __name__ == '__main__':
    fire.Fire()
