import CellularAutomaton, numpy, random

class FireGrid(CellularAutomaton.CAGrid):
#Note: 0 is empty, 1 is tree, 2 is burning
    #def __new__(cls, shape, *args, **kwargs):
    #    origcls = cls.__new__(shape, *args, **kwargs)
    #    origcls.ran = numpy.random.rand(origcls.shape[0], origcls.shape[1])
    #    return origcls
    #note: changed CAGrid to include this since it was breaking

    def Update(self):
        numpy.copyto(self.Old, self) # save old state, just in case
        numpy.place(self.count, self.TrueArray, 0) #0 out the count array

        for n in self.Neighbors:
            numpy.place(self.count,numpy.equal(n['State'],2), 1) #check if there are any burning neighbors

        #impliment burn rules
        #numpy.place(self['State'], self['State'] == 0, 0) #Empty Cells stay empty
        numpy.place(self['State'], numpy.equal(self['State'], 2), 0) #Burning Cells become empty
        numpy.place(self['State'], numpy.logical_and((self.count > 0), numpy.logical_and(numpy.equal(self['State'], 1), self.ran>0.25)), 2) #tree cells become burning if a neighbor is burning and they're not immune
        numpy.place(self['State'], numpy.logical_and(random.random()>0.99999, numpy.logical_and(numpy.equal(self['State'], 1), self.ran>0.25)), 2) #tree cells become burning if they're struck by lightning and not immune

        self.FinishUpdate()
        self.UpdateCount +=1


    def SetValue(self):
        for y in range(self.shape[0]):
            for x in range(self.shape[1]):
                if self['State'][y][x] == 2:
                    self['Value'][y][x] = (1, 0, 0)
                elif self['State'][y][x] == 1:
                    self['Value'][y][x] = (0, .75, 0)
                else:
                    self['Value'][y][x] = (.34, .231, .05)