import secrets as sc  
import numpy as np
import pandas as pd
import random

class dndChar:

    _xlsx = pd.ExcelFile("C:/Users/Noah/Documents/5E_CHARACTERSHEETSV3/Characters/CharacterGeneratorV2.xlsx")
    _rDataMaster = pd.read_excel(_xlsx,'Race')
    _cDataMaster = pd.read_excel(_xlsx,'Class')
    _bDataMaster = pd.read_excel(_xlsx,'Background')
    _sfile = open('C:/Users/Noah/Documents/5E_CHARACTERSHEETSV3/Characters/SNames.txt')
    _snamesfile = [line.replace('\n','') for line in _sfile]
    _mfile = open('C:/Users/Noah/Documents/5E_CHARACTERSHEETSV3/Characters/MNames.txt')
    _mnamesfile = [line.replace('\n','') for line in _mfile]
    _ffile = open('C:/Users/Noah/Documents/5E_CHARACTERSHEETSV3/Characters/FNames.txt')
    _fnamesfile = [line.replace('\n','') for line in _ffile]
    _statsMaster = ['strength','dexterity','constitution','intelligence','wisdom','charisma']

    def __init__(self):
        self.name = ['First', 'Last']
        self.race = ['Subrace', 'Race']
        self.raceRef = 0
        self.background = 'Background'
        self.backRef = 0
        self.gameClass = ['Subclass', 'Class']
        self.classRef = 0
        self.stats = {'strength': 0,
                      'dexterity': 0,
                      'constitution': 0,
                      'intelligence': 0,
                      'wisdom': 0, 
                      'charisma': 0}
        self.multiclass = [None,None]
        self.startingHP = 0
        self.rData = pd.DataFrame()
        self.cData = pd.DataFrame()
        self.bData = pd.DataFrame()
        self._cDataBackup = pd.DataFrame()

    def listUsedSources(self):
        """
        Lists sourcebooks generator pulls from
        """
        if self.cData.empty and self.rData.empty and self.bData.empty == True:
            raise Exception('No sources used')
        else:
            sourcelist = set(self.bData['Source'].unique())
            sourcelist.update(set(self.cData['Source'].unique()))
            sourcelist.update(set(self.rData['Source'].unique()))
            return sourcelist

    def listAvailableSources(self):
        """
        Lists sources not currently being used
        """
        sourcelist = set('')
        if not self.bData.empty:
            sourcelist.update(set(self._bDataMaster['Source'].unique()).difference(set(self.bData['Source'].unique())))
        if not self.cData.empty:
            sourcelist.update(set(self._cDataMaster['Source'].unique()).difference(set(self.cData['Source'].unique())))
        if not self.rData.empty:
            sourcelist.update(set(self._rDataMaster['Source'].unique()).difference(set(self.rData['Source'].unique())))
        if self.bData.empty and self.cData.empty and self.rData.empty:
            sourcelist.update(set(self._bDataMaster['Source'].unique()))
            sourcelist.update(set(self._cDataMaster['Source'].unique()))
            sourcelist.update(set(self._rDataMaster['Source'].unique()))
        return sourcelist

    def removeSource(self, targetSource):
        """
        Removes a source from list that the generator pulls from
        
        Parameters
        ----------
        targetSource: The source you want to remove as a string
        """
        self.bData = self.bData.drop(self.bData[self.bData['Source'] == targetSource].index)
        self.cData = self.cData.drop(self.cData[self.cData['Source'] == targetSource].index)
        self.rData = self.rData.drop(self.rData[self.rData['Source'] == targetSource].index)
        self._cDataBackup = self._cDataBackup.drop(self._cDataBackup[self._cDataBackup['Source'] == targetSource].index)

    def addSource(self, targetsource):
        """
        Adds an available source to the list the generator pulls from
        
        Parameters
        ----------
        Source: The source you want to add as a string
        """
        if self.bData.empty:
            self.bData = self.bData.append(self._bDataMaster.iloc[self._bDataMaster[self._bDataMaster['Source'] == targetsource].index])
        elif targetsource not in set(self.bData['Source'].unique()):
            self.bData = self.bData.append(self._bDataMaster.iloc[self._bDataMaster[self._bDataMaster['Source'] == targetsource].index],
                                            ignore_index=True)
        if self.cData.empty:
            self.cData = self.cData.append(self._cDataMaster.iloc[self._cDataMaster[self._cDataMaster['Source'] == targetsource].index])
        elif targetsource not in set(self.cData['Source'].unique()):
            self.cData = self.cData.append(self._cDataMaster.iloc[self._cDataMaster[self._cDataMaster['Source'] == targetsource].index],
                                            ignore_index=True)
        if self.rData.empty:
            self.rData = self.rData.append(self._rDataMaster.iloc[self._rDataMaster[self._rDataMaster['Source'] == targetsource].index])
        elif targetsource not in set(self.rData['Source'].unique()):
            self.rData = self.rData.append(self._rDataMaster.iloc[self._rDataMaster[self._rDataMaster['Source'] == targetsource].index],
                                            ignore_index=True)
        if self._cDataBackup.empty:
            self._cDataBackup = self._cDataBackup.append(self._cDataMaster.iloc[self._cDataMaster[self._cDataMaster['Source'] == targetsource].index])
        elif targetsource not in set(self._cDataBackup['Source'].unique()):
            self._cDataBackup = self._cDataBackup.append(self._cDataMaster.iloc[self._cDataMaster[self._cDataMaster['Source'] == targetsource].index],
                                            ignore_index=True)

    def addAllSources(self):
        """
        Allows the generator to pull from all available sources
        """
        self.bData = self._bDataMaster.copy()
        self.cData = self._cDataMaster.copy()
        self.rData = self._rDataMaster.copy()
        self._cDataBackup = self._cDataMaster.copy()

    def resetSources(self):
        """
        Removes all available sources from the generator's list
        """
        self.rData = pd.DataFrame()
        self.cData = pd.DataFrame()
        self.bData = pd.DataFrame()
        self._cDataBackup = pd.DataFrame()

    def assignRandClass(self):
        """
        Randomly sets the character's class from the list of available classes
        """
        self.classRef = sc.randbelow(len(self.cData.index))
        self.gameClass = [self.cData.iloc[self.classRef][1], self.cData.iloc[self.classRef][0]]

    def assignClass(self,chosenClass,chosenSubclass):
        """
        Sets the character's class and subclass from the list of available classes

        Parameters
        ----------
        chosenClass: String: Must match a class available to the generator

        chosenSubclass: String: Must match a subclass available to the generator
        """
        pass

    def resetClassRestricts(self):
        """
        Removes restrictions placed on available classes
        """
        if not self._cDataBackup.empty:
            self.cData = self._cDataBackup.copy()
        else:
            raise Exception('No sources found to restore')

    def restrictCasters(self, full=0, half=0, third=0, non=0):
        """
        Removes selected class options from generator list
        
        Parameters
        ----------
        full: Removes full casters on 1, keeps on 0

        half: Removes half casters on 1, keeps on 0

        third: Removes 1/3 casters on 1, keeps on 0

        non: Removes noncasters on 1, keeps on 0

        Warlocks are considered noncasters
        """
        removeList = [999]
        if full == 1:
            removeList.append(np.int64(1))
        if half == 1:
            removeList.append(np.int64(2))
        if third == 1:
            removeList.append(np.int64(3))
        if non == 1:
            removeList.append(np.int64(0))
        self.cDataBackupTemp = self.cData.copy()
        for n in removeList:
            self.cData = self.cData.drop(self.cData[self.cData['Caster'] == n].index)
        if self.cData.empty:
            print('All classes removed. Repopulating list...')
            self.cData = self.cDataBackupTemp.copy()

    def restrictBySelectedClass(self, targetClass, exclude=0):
        """
        Restricts class options by the entered class
        
        Parameters
        ----------
        targetClass: string, the class targeted

        exclude: int, 0: Removes targetClass 
                  1: Removes all classes NOT matching targetClass
        """
        self.cDataBackupTemp = self.cData.copy()
        if exclude == 1:
            self.cData = self.cData.drop(self.cData[self.cData['Class'] != targetClass].index)
            if self.cData.empty:
                print('All classes removed. Repopulating list...')
                self.cData = self.cDataBackupTemp.copy()
        else:
            self.cData = self.cData.drop(self.cData[self.cData['Class'] == targetClass].index)
            if self.cData.empty:
                print('All classes removed. Repopulating list...')
                self.cData = self.cDataBackupTemp.copy()

    def restrictPrimaryStat(self, stat, exclude=0):
        """
        Restricts class options to those which prioritize the selected stat
        
        Parameters
        ----------
        stat: string, chosen from strength, dexterity, constitution, intelligence, wisdom, and charisma
        exclude: int, 0: Removes stat 
                  1: Removes all classes NOT matching stat
        """
        self.cDataBackupTemp = self.cData.copy()
        if exclude == 1:
            cDataTemp = pd.DataFrame()
            cDataTemp = cDataTemp.append(self.cData.loc[self.cData[self.cData['Primary Stat'] == stat].index])
            cDataTemp = cDataTemp.append(self.cData.loc[self.cData[self.cData['Primary Stat Alt'] == stat].index])
            self.cData = cDataTemp.copy()
            if self.cData.empty:
                print('All classes removed. Repopulating list...')
                self.cData = self.cDataBackupTemp.copy()
        else:
            self.cData = self.cData.drop(self.cData[self.cData['Primary Stat'] == stat].index)
            self.cData = self.cData.drop(self.cData[self.cData['Primary Stat Alt'] == stat].index)
            if self.cData.empty:
                print('All classes removed. Repopulating list...')
                self.cData = self.cDataBackupTemp.copy()

    def restrictCRole(self, role, exclude=0):
        """
        Restricts class options to those which prioritize the selected combat role 
        
        Parameters
        ----------
        role: string, chosen from tank, dps, control, and support
        exclude: int, 0: Removes targetClass 
                  1: Removes all classes NOT matching targetClass
        """
        self.cDataBackupTemp = self.cData.copy()
        if exclude == 1:
            self.cData = self.cData.drop(self.cData[self.cData['CRole'] != role].index)
            if self.cData.empty:
                print('All classes removed. Repopulating list...')
                self.cData = self.cDataBackupTemp.copy()
        else:
            self.cData = self.cData.drop(self.cData[self.cData['CRole'] == role].index)
            if self.cData.empty:
                print('All classes removed. Repopulating list...')
                self.cData = self.cDataBackupTemp.copy()

    def restrictURole(self, role,exclude=0):
        """
        Restricts class options to those which prioritize the selected utility role
        
        Parameters
        ----------
        role: string, chosen from face, skill, sneak, and muscle
        exclude: int, 0: Removes targetClass 
                  1: Removes all classes NOT matching targetClass
        """
        self.cDataBackupTemp = self.cData.copy()
        if exclude == 1:
            self.cData = self.cData.drop(self.cData[self.cData['URole'] != role].index)
            if self.cData.empty:
                print('All classes removed. Repopulating list...')
                self.cData = self.cDataBackupTemp.copy()
        else:
            self.cData = self.cData.drop(self.cData[self.cData['URole'] == role].index)
            if self.cData.empty:
                print('All classes removed. Repopulating list...')
                self.cData = self.cDataBackupTemp.copy()

    def assignStats(self, assignMethod=0):
        """
        Assigns stats to character, prioritizing those valued by the class.

        Stat points from race allotted by player choice are NOT assigned here except half-elf in point-buy.
        
        Parameters
        ----------
        assignMethod: int, selects the method of stat allocation to be used

            0: the standard array given by PHB

            1: a point-buy spread as allowed by PHB
        """
        if self.gameClass == ['Subclass', 'Class']:
            raise Exception('Please set class prior to stat allocation')
        if self.race == ['Subrace', 'Race']:
            raise Exception('Please set race prior to stat allocation')

        allStats = self._statsMaster.copy()
        highStat = []
        highStat.append(str(self.cData.iloc[self.classRef]['Primary Stat']))
        if str(self.cData.iloc[self.classRef]['Primary Stat Alt']) != 'nan': 
            highStat.append(str(self.cData.iloc[self.classRef]['Primary Stat Alt']))
        highStatSelect = sc.randbelow(len(highStat))
        highStat = highStat[highStatSelect]
        allStats.remove(highStat)

        twoStat = []
        twoStat.append(str(self.cData.iloc[self.classRef]['Secondary Stat']))
        if str(self.cData.iloc[self.classRef]['Secondary Stat Alt']) != 'nan': 
            twoStat.append(str(self.cData.iloc[self.classRef]['Secondary Stat Alt']))
        if highStat in twoStat:
            twoStat.remove(highStat)
        twoStatSelect = sc.randbelow(len(twoStat))
        twoStat = twoStat[twoStatSelect]
        allStats.remove(twoStat)

        if assignMethod == 0:
            standardArray = [15,14,13,12,10,8]
            self.stats[highStat] = standardArray[0]
            standardArray.pop(0)
            self.stats[twoStat] = standardArray[0]
            standardArray.pop(0)
            random.shuffle(standardArray)
            for n in allStats:
                self.stats[n] = standardArray[0]
                standardArray.pop(0)
            for n in self._statsMaster:
                if str(self.rData.iloc[self.raceRef][n]) != 'nan':
                    self.stats[n] += int(self.rData.iloc[self.raceRef][n])
            self._setStartingHP()
        else:
            if self.race == ['Human']:
                statArrays = [[15, 13, 13, 13, 11, 8],
                              [15, 13, 13, 13, 10, 9],
                              [15, 13, 13, 12, 11, 9],
                              [15, 13, 13, 11, 11, 10],
                              [15, 13, 12, 11, 11, 11],
                              [14, 13, 13, 13, 11, 10],
                              [13, 13, 13, 13, 13, 10],
                              [13, 13, 13, 13, 12, 11]]
                statArray = statArrays[sc.randbelow(len(statArrays))]
                self.stats[highStat] = statArray[0]+1
                statArray.pop(0)
                self.stats[twoStat] = statArray[0]+1
                statArray.pop(0)
                random.shuffle(statArray)
                for n in allStats:
                    self.stats[n] = statArray[0]+1
                    statArray.pop(0)
                self._setStartingHP()
            elif self.race == ['Half-Elf'] or self.race == ['Aetherborn']:
                statArrays = []
                if highStat == 'charisma' or twoStat == 'charisma':
                    statArrays = [[16,16,16,10,8,8],
                                  [16,16,14,12,10,8]]
                    statArray = statArrays[sc.randbelow(len(statArrays))]
                    self.stats[highStat] = statArray[0]
                    statArray.pop(0)
                    self.stats[twoStat] = statArray[0]
                    statArray.pop(0)
                    random.shuffle(statArray)
                    for n in allStats:
                        self.stats[n] = statArray[0]
                        statArray.pop(0)
                    self._setStartingHP()
                else:
                    statArrays = [[16,16,14,10,8,8],
                                  [16,14,14,12,10,8]]
                    statArray = statArrays[sc.randbelow(len(statArrays))]
                    self.stats[highStat] = statArray[0]
                    statArray.pop(0)
                    self.stats[twoStat] = statArray[0]
                    statArray.pop(0)
                    random.shuffle(statArray)
                    for n in allStats:
                        self.stats[n] = statArray[0]
                        if n == 'charisma':
                            self.stats[n] += 2
                        statArray.pop(0)
                    self._setStartingHP()
            else:
                statArrays = [[14, 14, 14, 12, 10, 8],
                              [14, 14, 14, 10, 10, 10],
                              [14, 12, 12, 12, 12, 12],
                              [15, 15, 13, 10, 10, 8],
                              [15, 14, 14, 12, 8, 8],
                              [15, 14, 14, 10, 10, 8],
                              [15, 14, 13, 12, 10, 8],
                              [15, 14, 13, 10, 10, 10],
                              [15, 14, 12, 12, 11, 8],
                              [15, 14, 12, 12, 10, 9],
                              [15, 14, 12, 11, 10, 10],
                              [15, 13, 13, 12, 10, 10],
                              [15, 13, 12, 12, 12, 9],
                              [15, 13, 12, 12, 11, 10],
                              [15, 12, 12, 12, 12, 10],
                              [15, 12, 12, 12, 11, 11]]
                statArray = statArrays[sc.randbelow(len(statArrays))]
                self.stats[highStat] = statArray[0]
                statArray.pop(0)
                self.stats[twoStat] = statArray[0]
                statArray.pop(0)
                random.shuffle(statArray)
                for n in allStats:
                    self.stats[n] = statArray[0]
                    statArray.pop(0)
                    if str(self.rData.iloc[self.raceRef][n]) != 'nan':
                        self.stats[n] += int(self.rData.iloc[self.raceRef][n])
                self._setStartingHP()

    def resetStats(self):
        """
        Undoes stat assignment
        """
        self.stats = {'strength': 0,
                      'dexterity': 0,
                      'constitution': 0,
                      'intelligence': 0,
                      'wisdom': 0, 
                      'charisma': 0}

    def addRandMulticlass(self):
        """
        Adds a random secondary class which the character qualifies for
        """
        pass

    def addMulticlass(self,chosenClass,chosenSubclass):
        """
        Sets the character's second class and subclass from the list of available classes

        Parameters
        ----------
        chosenClass: String: Must match a class available to the generator

        chosenSubclass: String: Must match a subclass available to the generator
        """
        pass

    def removeMulticlass(self):
        """
        Removes any secondary classes the character may have
        """
        self.multiclass = [None,None]

    def generateName(self, gender=2):
        """
        Generates a character name
        
        Parameters
        ----------
        gender: int: 0=female, 1=male, 2=unrestricted

        Output
        --------
        ['first', 'last']
        """
        name1 = None
        name2 = self._snamesfile[sc.randbelow(len(self._snamesfile))]
        if gender == 2:
            gender = sc.randbelow(2)
        if gender == 0:
            name1 = self._fnamesfile[sc.randbelow(len(self._fnamesfile))]
        elif gender == 1:
            name1 = self._mnamesfile[sc.randbelow(len(self._mnamesfile))]
        self.name = [name1, name2] 

    def resetChar(self):
        """
        Resets the current character
        """
        self.name = ['First', 'Last']
        self.race = ['Subrace', 'Race']
        self.raceRef = 0
        self.background = 'Background'
        self.backRef = 0
        self.gameClass = ['Subclass', 'Class']
        self.classRef = 0
        self.stats = {'strength': 0,
                      'dexterity': 0,
                      'constitution': 0,
                      'intelligence': 0,
                      'wisdom': 0, 
                      'charisma': 0}
        self.multiclass = [None,None]
        self.startingHP = 0

    def _setStartingHP(self):
        """
        Sets the starting HP of the character
        """
        conmod = (self.stats['constitution']-10)//2
        self.startingHP = conmod+int(self.cData.iloc[self.classRef]['Hit Die'])

    def setRandBackground(self):
        """
        Sets a random background for the character
        """
        self.backRef = sc.randbelow(len(self.bData.index))
        self.background = str(self.bData.iloc[self.backRef][0])

    def setBackground(self,chosenBackground):
        """
        Sets the character's background from the list of available backgrounds

        Parameters
        ----------
        chosenBackground: String: Must match a background available to the generator
        """
        pass

    def setRandRace(self):
        """
        Randomly sets the character's race
        """
        self.raceRef = sc.randbelow(len(self.rData.index))
        self.race = [self.rData.iloc[self.raceRef][1], self.rData.iloc[self.raceRef][0]]
        if type(self.race[0]) != str:
            self.race = [self.race[1]]

    def setRace(self,chosenRace, chosenSubrace=0):
        """
        Sets the character's race and subrace from the list of available races

        Parameters
        ----------
        chosenRace: String: Must match a race available to the generator

        chosenSubrace: String: Must match a subrace available to the generator. Leave blank if no subrace
        """
        pass

    def viewCharacter(self):
        """
        Prints relevant information about the character
        """
        print('Name: %s %s' %(self.name[0], self.name[1]))
        if len(self.race) == 1:
            print('Race: %s' %(self.race[0]))
        else:
            print('Race: %s %s' %(self.race[0],self.race[1]))
        print('Background: '+self.background)
        print('Class: %s %s' %(self.gameClass[0], self.gameClass[1]))
        if self.multiclass[0] != None:
            print('Multiclass: %s %s' %(self.multiclass[0], self.multiclass[1]))
        print('STR: '+str(self.stats['strength']))
        print('DEX: '+str(self.stats['dexterity']))
        print('CON: '+str(self.stats['constitution']))
        print('INT: '+str(self.stats['intelligence']))
        print('WIS: '+str(self.stats['wisdom']))
        print('CHA: '+str(self.stats['charisma']))
        print('Starting HP: %s' %(str(self.startingHP)))

