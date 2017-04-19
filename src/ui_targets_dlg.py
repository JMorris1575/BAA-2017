from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Module Level Functions--------------------------------------------------------

def decimalFormat(n, mode=None):
    ns = '{0:.2f}'.format(round(n*1.0, 2)) # ns = string rounded to 2 decimals
    dPart = ns[-3:]     # save the decimal part
    count=0
    fs = ''
    for char in ns[ns.find('.')-1::-1]:
        fs = char + fs
        count += 1
        if count==3:
            fs = ',' + fs
            count = 0
    if fs[0:1] == ',':
        fs = fs[1:]
    if mode == 'dollars':
        fs = '$' + fs + dPart
    elif mode == 'percent':
        fs = fs + dPart + '%'
    return fs

def cleanNumber(inString):
    outString = ""
    for char in inString:
        if char.isnumeric() or char == ".":
            outString += char
    return outString

def String2Num(s):
    numchar = '0123456789.'
    s2 = ''
    for char in s:
        if char in numchar:
            s2 += char
    return(float(s2))

def testForNumbers(nString, numType):
    # tries to convert nString to the indicated numeric type
    # and returns whether it was successful or not
    clean = cleanNumber(nString)
    validNumber = True
    try:
        if numType == 'float':
            float(clean)
        if numType == 'int':
            int(clean)
    except ValueError:
        validNumber = False
    return validNumber


class TargetsDlgSetup(QDialog):

    def __init__(self, targets, parent=None):
        super(TargetsDlgSetup, self).__init__(parent)
        self.targets = targets
        self.setup()
        self.show()

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
        self.goalEdit.setText(decimalFormat(self.targets["goal"], 'dollars'))
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
        dlgButtonBox.accepted.connect(self.okClicked)
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

    def okClicked(self):
        """
        This is where you can do some input checking
        :return: 
        """

        class YearError(Exception):
            pass

        class GoalError(Exception):
            pass

        class FamiliesError(Exception):
            pass

        year = self.yearEdit.text()
        goal = self.goalEdit.text()
        families = self.familyEdit.text()
        try:
            if len(year) == 0:
                raise YearError("Are you sure you don't want to include the year in the heading?")

            if len(goal) == 0:
                raise GoalError('You must enter the target goal for this year.')
            if String2Num(goal) <= 0.0:
                raise GoalError('The goal must be greater than zero.')
            try:
                testForNumbers(goal, 'float')
            except ValueError:
                raise GoalError('The goal must be a numeric value.')

            if len(families) == 0:
                raise FamiliesError('You must enter the number of families\n' +
                                    'in the parish.')
            if int(String2Num(families)) <= 0:
                raise FamiliesError('You must enter the number of families\n' +
                                    'in the parish.')

            try:
                testForNumbers(families, 'int')
            except ValueError:
                raise FamiliesError('The number of families must be\n' +
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
        except FamiliesError as e:
            QMessageBox.warning(self, "Families Error", str(e))
            self.familyEdit.selectAll()
            self.familyEdit.setFocus()
            return

        self.targets['year'] = year
        self.targets['goal'] = decimalFormat(float(cleanNumber(goal)), 'dollars')
        self.targets['families'] = families

        self.accept()

# End of TargetsDlgSetup -------------------------------------------------------


class EditTargetsDlg(TargetsDlgSetup):

    def __init__(self, targets, parent=None):
        super(EditTargetsDlg, self).__init__(targets, parent)
        self.targets = targets
        # self.setupUi(self)
        # self.connect(self.buttonBox, SIGNAL("accepted()"),
        #              self, SLOT("self.accept()"))
        # self.connect(self.buttonBox, SIGNAL("rejected()"),
        #              self, SLOT("self.reject()"))

        # if self.targets['year'] is not None:
        #     self.yearSpinBox.setValue(int(self.targets['year']))
        #     self.goalLineEdit.setText(self.targets['goal'])
        #     self.totalFamiliesLineEdit.setText(self.targets['families'])
        #
        # self.yearSpinBox.setFocus()

    def getTargets(self):
        return self.targets

    def accept(self):
        class YearError(Exception):
            pass

        class GoalError(Exception):
            pass

        class FamiliesError(Exception):
            pass

        # year = str(self.yearSpinBox.value())
        # goal = self.goalLineEdit.text()
        # families = self.totalFamiliesLineEdit.text()
        # try:
        #     if len(goal) == 0:
        #         raise GoalError('You must enter the target goal for this year.')
        #     try:
        #         testForNumbers(goal, 'float')
        #     except ValueError:
        #         raise GoalError('The goal must be a numeric value.')
        #     if len(families) == 0:
        #         raise FamiliesError('You must enter the number of families\n' +
        #                             'in the parish.')
        #     try:
        #         testForNumbers(families, 'int')
        #     except ValueError:
        #         raise FamiliesError('The number of families must be\n' +
        #                             'an integer.  Example: 1403')
        # except GoalError as e:
        #     QMessageBox.warning(self, "Goal Error", str(e))
        #     self.goalLineEdit.selectAll()
        #     self.goalLineEdit.setFocus()
        #     return
        # except FamiliesError as e:
        #     QMessageBox.warning(self, "Families Error", str(e))
        #     self.totalFamiliesLineEdit.selectAll()
        #     self.totalFamiliesLineEdit.setFocus()
        #     return
        #
        # self.targets['year'] = year
        # self.targets['goal'] = decimalFormat(float(cleanNumber(goal)), 'dollars')
        # self.targets['families'] = families
        #
        print("Hi!")
        QDialog.accept(self)

# End of TargetsEditDlg Class---------------------------------------------------
