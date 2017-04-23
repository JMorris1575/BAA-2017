from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import helperFunctions


class EditTargetsDlg(QDialog):

    # ToDo: set focus to the yearEdit box upon entry
    # ToDo: check to see if it gracefully handles all forms of user input

    def __init__(self, targets, parent=None):
        super(EditTargetsDlg, self).__init__(parent)
        self.targets = targets
        self.setup()

    def setup(self):
        self.resize(260, 150)

        yearLabel = QLabel("Campaign Year:")
        self.yearEdit = QLineEdit()
        self.yearEdit.setText(self.targets["year"])
        self.yearEdit.setToolTip('Enter the year part of the heading for the final graphic.')
        self.yearEdit.setWhatsThis('Enter a year or a range of years. What you enter here will appear as' +
                                   'part of the heading of the final graphic.')
        yearBoxLayout = QHBoxLayout()
        yearBoxLayout.addStretch()
        yearBoxLayout.addWidget(yearLabel)
        yearBoxLayout.addWidget(self.yearEdit)

        goalLabel = QLabel("Campaign Goal:")
        self.goalEdit = QLineEdit()
        self.goalEdit.setText(helperFunctions.decimalFormat(self.targets["goal"], 'dollars'))
        self.goalEdit.setToolTip("Enter the parish goal for the Bishop's Annual Appeal.")
        self.goalEdit.setWhatsThis("Set the goal for this year's Bishop's Annual Appeal. You may enter it formatted " +
                                   "as dollars and cents ($12,345.67) or simply enter the digits (12345.67).")
        goalBoxLayout = QHBoxLayout()
        goalBoxLayout.addStretch()
        goalBoxLayout.addWidget(goalLabel)
        goalBoxLayout.addWidget(self.goalEdit)

        familyLabel = QLabel("Total Family Count:")
        self.familyEdit = QLineEdit()
        self.familyEdit.setText(str(self.targets["families"]))
        self.familyEdit.setToolTip('Enter the number of families in the parish.')
        self.familyEdit.setWhatsThis('Enter the number of families in the parish. This is used to display the ' +
                                     "percentage of families participating in this year's Bishop's Annual Appeal.")
        familyBoxLayout = QHBoxLayout()
        familyBoxLayout.addStretch()
        familyBoxLayout.addWidget(familyLabel)
        familyBoxLayout.addWidget(self.familyEdit)

        dlgButtonBox = QDialogButtonBox(QDialogButtonBox.Cancel|QDialogButtonBox.Ok, Qt.Horizontal, self)
        dlgButtonBox.accepted.connect(self.accept)
        dlgButtonBox.rejected.connect(self.reject)
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(dlgButtonBox)

        layout = QVBoxLayout(self)
        layout.addLayout(yearBoxLayout)
        layout.addLayout(goalBoxLayout)
        layout.addLayout(familyBoxLayout)
        layout.addStretch()
        layout.addLayout(buttonLayout)

    def getTargets(self):
        return self.targets

    def accept(self):

        class YearError(Exception):pass

        class GoalError(Exception):pass

        class FamilyError(Exception):pass

        year = self.yearEdit.text()
        goal = self.goalEdit.text()
        families = self.familyEdit.text()
        try:
            if len(year) == 0:
                raise YearError("Are you sure you don't want to include the year in the heading?")

            if len(goal) == 0:
                raise GoalError('You must enter the target goal for this year.')
            if helperFunctions.String2Num(goal) <= 0.0:
                raise GoalError('The goal must be greater than zero.')
            try:
                helperFunctions.testForNumbers(goal, 'float')
            except ValueError:
                raise GoalError('The goal must be a numeric value.')

            if len(families) == 0:
                raise FamilyError('You must enter the number of families\n' +
                                    'in the parish.')
            if int(helperFunctions.String2Num(families)) <= 0:
                raise FamilyError('You must enter the number of families\n' +
                                    'in the parish.')

            try:
                helperFunctions.testForNumbers(families, 'int')
            except ValueError:
                raise FamilyError('The number of families must be\n' +
                                    'an integer.  Example: 1403')
        except YearError as e:
            response = QMessageBox.question(self, "Year Error?", str(e))
            if response == QMessageBox.Yes:
                pass
            elif response == QMessageBox.No:
                self.yearEdit.selectAll()
                self.yearEdit.setFocus()
                return
        except GoalError as e:
            QMessageBox.warning(self, "Goal Error", str(e))
            self.goalEdit.selectAll()
            self.goalEdit.setFocus()
            return
        except FamilyError as e:
            QMessageBox.warning(self, "Families Error", str(e))
            self.familyEdit.selectAll()
            self.familyEdit.setFocus()
            return

        self.targets['year'] = year
        self.targets['goal'] = float(helperFunctions.cleanNumber(goal))
        self.targets['families'] = int(helperFunctions.cleanNumber(families))
        self.targets['set'] = True

        QDialog.accept(self)

# End of TargetsEditDlg Class---------------------------------------------------
