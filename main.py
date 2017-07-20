from scipy.optimize import linear_sum_assignment
import csv
import numpy as np

# Algorithm: This committee assignment uses SciPy's linear sum assignment, 
#            which solves for the minimum weight matching in a bipartite graph
#
# Approach: In a bipartite graph (P,C), nodes in P are people, and nodes in C are
#           spots in a committee (i.e X committee may have N spots, so there are N
#           nodes for committee X in C). The weights on the edges represent a person's 
#           preference for those committee's spots. First choice gives weight of 0,
#           second choice weight of 1, and so on. 

class Person():

    def __init__(self, csv_row):
        self.timestamp = csv_row[0]
        self.email = csv_row[1]
        self.name = csv_row[2]
        self.andrewID = csv_row[3]
        self.year = csv_row[4]
        self.choices = [csv_row[i] for i in range(5,11)]
        self.assignment = None


class CommitteeAssignment():

    def __init__(self, path):
        # self.comm_sizes = {
        #     "Social": 9,
        #     "Brotherhood": 8,
        #     "Philanthropy": 7,
        #     "Community Service": 3,
        #     "Outreach": 3,
        #     "Recruitment": 12,
        #     "Phi Ed": 7,
        #     "Greek Sing": 6,
        #     "Housing": 6,
        #     "Scholarship": 6,
        #     "Risk": 5,
        #     "Buggy": 5,
        #     "Bylaws": 3
        # }
        self.num_choices = 6
        self.path = path

        self.comm_sizes = {
            "Social": 2,
            "Brotherhood": 2,
            "Philanthropy": 2,
            "Community Service": 2,
            "Outreach": 2,
            "Recruitment": 2,
            "Phi Ed": 2,
            "Greek Sing": 2,
            "Housing": 2,
            "Scholarship": 2,
            "Risk": 1,
            "Buggy": 1,
            "Bylaws": 1
        }

        self.comm_indexes = self.makeCommitteeIndexes() # used for cost matrix


    def makeCommitteeIndexes(self):
        comm_indexes = dict()
        idx = 0
        for committee in self.comm_sizes:
            comm_indexes[committee] = list(range(idx, idx+self.comm_sizes[committee]))
            idx += self.comm_sizes[committee]
        return comm_indexes


    def makeCostMatrix(self):
        costs = np.full((len(self.people), sum(self.comm_sizes.values())), self.num_choices)
        for i in range(len(self.people)):
            person = self.people[i]
            for j in range(len(person.choices)):
                committee = person.choices[j]
                costs[i,self.comm_indexes[committee]] = j
        return costs


    def makeAssignments(self):
        row_ind, col_ind = linear_sum_assignment(self.costs)
        for i in range(len(self.people)):
            self.people[i].assignment = self.getAssignmentFromIndex(col_ind[i]) 


    def getAssignmentFromIndex(self, index):
        for committee in self.comm_indexes:
            if index in self.comm_indexes[committee]:
                return committee


    def printAssignments(self):
        for person in self.people:
            print("{} : {}".format(person.name, person.assignment))


    def printAssignmentReport(self):
        switcher = {
            0: " people got their 1st choice",
            1: " people got their 2nd choice",
            2: " people got their 3rd choice",
            3: " people got their 4th choice",
            4: " people got their 5th choice",
            5: " people got their 6th choice",
            6: " people got their none of their choices"
        }
        for i in range(self.num_choices + 1):
            num_people = 0
            for person in self.people:
                if i < self.num_choices and person.assignment == person.choices[i]:
                    num_people += 1
            print(str(num_people) + switcher[i])


    def run(self):

        with open(self.path, "r", encoding='utf-8') as file:
            self.csv_file = list(csv.reader(file))

        self.people = [Person(row) for row in self.csv_file[1:]]

        self.costs = self.makeCostMatrix()

        self.makeAssignments()

        self.printAssignments()

        self.printAssignmentReport()


if __name__ == '__main__':
    CommitteeAssignment("preferences.csv").run()