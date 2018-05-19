import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

class VisualStimData:
    """
    Data and methods for the visual stimulus ePhys experiment.
    The data table itself is held in self.data, an `xarray` object.
    Inputs:
        data: xr.DataArray or xr.Dataset
        ...
    Methods:
        plot_electrode
        experimenter_bias
         ...
    """
    def __init__(self, data):
        self.data = data

    def plot_electrode(self, rep_number: int, rat_id: int, elec_number: tuple=(0,)):
        """
        Plots the voltage of the electrodes in "elec_number" for the rat "rat_id" in the repetition
        "rep_number". Shows a single figure with subplots.
        """
        electrodes = [[0,1000],[1000,2000],[2000,3000],[3000,4000],[4000,5000],[5000,6000],[6000,7000],[7000,8000],[8000,9000],[9000,10000]]
        rat_values = self.data[rat_id].sel(rep_num=rep_number).values
        fig, ax = plt.subplots(2,5)
        x = 0
        y = 0
        for elec in elec_number:
            elec_values = rat_values[electrodes[elec-1][0]:electrodes[elec-1][1]]
            elec_x = np.arange(1,len(elec_values)+1)
            ax[x,y].plot(elec_x,elec_values)
            ax[x,y].set_title(f"electrode {elec}")
            y = y + 1
            if y==5:
                x += 1
                y = 0
        plt.show()

    def experimenter_bias(self):
        """ Shows the statistics of the average recording across all experimenters """
        mean_values=[]
        std_values=[]
        median_values=[]
        exp_names = ['Daniel','Anna']
        rat_ids = np.arange(1,10)
        for name in exp_names:
            name_values = []
            for rat in rat_ids:
                if name == self.data[rat].attrs['Experimenter']:
                    name_values.append(float(self.data[rat].mean().values))
            mean_values.append(np.mean(name_values))
            std_values.append(np.std(name_values))
            median_values.append(np.median(name_values))
        fig, ax = plt.subplots(1,3)
        ax[0].bar(exp_names,mean_values)
        ax[0].set_title('Mean')
        ax[1].bar(exp_names,std_values)
        ax[1].set_title('Standard deviation')
        ax[2].bar(exp_names,median_values)
        ax[2].set_title('Median')
        plt.show()

        
def mock_stim_data() -> VisualStimData:
    """ Creates a new VisualStimData instance with mock data """
    rat_ids = np.arange(1,10)
    room_temp = '25'
    room_humidity = '20'
    exp_names = ['Daniel','Anna']
    rat_genders = ['Male','Female']
    a = np.arange(10000)
    b = (['pre_']*500+['dur_']*50+['post_']*450)*10
    stim_index = []
    for x in range(0,(len(b))):
        stim_index.append(b[x]+str(a[x]))
    rep_num = np.arange(4)
    dims = ('stim_index','rep_num')
    coords = {'stim_index': stim_index, 'rep_num': rep_num}
    temp_data = xr.Dataset()
    for rat in rat_ids:
        exp_name = np.random.choice(exp_names)
        rat_gender = np.random.choice(rat_genders)
        voltage = np.random.random((10000, 4))
        data_array = xr.DataArray(voltage,dims=dims,coords=coords,attrs={'RatID': rat, 'Room_temp': room_temp, 'Room_humidity': room_humidity, 'Experimenter': exp_name, 'Rat_gender': rat_gender})
        temp_data[rat] = data_array
    mock_data = VisualStimData(temp_data)
    return mock_data


if __name__ == '__main__':
    stim_data = mock_stim_data()
    stim_data.plot_electrode(rep_number=2, rat_id=4, elec_number=(1,3,7))
    stim_data.experimenter_bias()
