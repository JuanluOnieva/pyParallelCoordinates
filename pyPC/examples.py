
"""
    Main Script
    author: Juan L. Onieva
"""

from ParallelCoordinates import ParallelCoordinates


def run():
    """
    Exute the necessary instruction in order to get the corresponding file plots of different data.
    It saves the plot with different format in the default directory
    :return:
    """
    # Create object
    pc_iris = ParallelCoordinates('data/iris.csv', header='infer', my_delimiter=',')
    pc_fun = ParallelCoordinates('data/FUN.BB20002.tsv', my_delimiter='\t')
    pc_mm = ParallelCoordinates('data/MaF14PF_M10.txt', my_delimiter=' ')

    # Plot as Parallel Coordinates
    pc_iris.plot(title='IRIS', show=False)
    pc_fun.plot(title='FUN.BB20002', show=False, normalize=True)
    pc_mm.plot(title='MaF14PF_M10', show=False)

    # Save with different formats
    pc_iris.save(file_name='IRIS', format='png')
    pc_fun.save(file_name='FUN')
    pc_mm.save(file_name='MaF14PF_M10', format='svg')


if __name__== "__main__":
    run()
