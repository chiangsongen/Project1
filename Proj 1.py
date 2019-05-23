import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()

sat_2017 = '../Classes_clone/projects1234/project_1/data/sat_2017.csv'
act_2017 = '../Classes_clone/projects1234/project_1/data/act_2017.csv'
sat_2018 = '../Classes_clone/projects1234/project_1/data/sat_2018.csv'
act_2018 = '../Classes_clone/projects1234/project_1/data/act_2018.csv'

with open(sat_2017, mode="r") as sat17:
    sat17 = pd.read_csv(sat17)

with open(act_2017, mode="r") as act17:
    act17 = pd.read_csv(act17)

with open(sat_2018, mode="r") as sat18:
    sat18 = pd.read_csv(sat18)

with open(act_2018, mode="r") as act18:
    act18 = pd.read_csv(act18)

sat17.loc[(sat17.State == "Maryland") & (sat17.Participation == "69%") & (sat17.Total == 1060), "Math"] = 524
act17.loc[(act17.State == "Maryland") & (act17.Participation == "28%") & (act17.Composite == "23.6"), "Science"] = 23.2
act17.loc[(act17.State == "Wyoming") & (act17.Participation == "100%") & (act17.English == 19.4), "Composite"] = 20.2
# act17.Composite.dtypes should be float64 as well, similar to Science or Reading
# act17 and sat17 Participication.dtypes shld be float64

sat17["Participation"] = [x[:-1] for x in sat17["Participation"]] # To remove '%' from the last character
act17["Participation"] = [x[:-1] for x in act17["Participation"]] # To remove '%' from the last character

sat18["Participation"] = [x[:-1] for x in sat18["Participation"]] # To remove '%' from the last character
#act18["Participation"] = [x[:-1] for x in act18["Participation"]] # To remove '%' from the last character

def coerce_df_columns_to_numeric(df, column_list):
    df[column_list] = df[column_list].apply(pd.to_numeric, errors='coerce')
    return df

coerce_df_columns_to_numeric(sat17, "Participation")                # To convert string to int or float
coerce_df_columns_to_numeric(act17, ["Participation", "Composite"]) # To convert string to int or float
coerce_df_columns_to_numeric(sat18, "Participation")                # To convert string to int or float

sat17["Participation"] = [x/100 for x in sat17["Participation"]] # To change it to %
act17["Participation"] = [x/100 for x in act17["Participation"]] # To change it to %

sat18["Participation"] = [x/100 for x in sat18["Participation"]] # To change it to %
act18["Participation"] = [x/100 for x in act18["Participation"]] # To change it to %

sat17.columns = ['state', 'participation_s17', 'erw_s17', 'math_s17', 'total_s17']                                    # change col names
act17.columns = ['state', 'participation_a17', 'eng_a17', 'math_a17', 'readg_a17', 'science_a17', 'composite_a17']    # change col names
sat18.columns = ['state', 'participation_s18', 'erw_s18', 'math_s18', 'total_s18']                                    # change col names
act18.columns = ['state', 'participation_a18', 'eng_a18', 'math_a18', 'readg_a18', 'science_a18', 'composite_a18']    # change col names

act17 = act17.set_index("state")        # Set index to 'state' col in order to drop row with index 'National'
act17 = act17.drop("National", axis=0)

act18 = act18.set_index("state")        # Set index to 'state' col in order to drop row with index 'National'
act18 = act18.drop("National", axis=0)

combine_17 = sat17.join(act17, on="state") # Joing sat17 and act17, by using index 'state'
combine_17.to_csv('../Classes_clone/projects1234/project_1/data/combine_2017.csv', index = None, header=True) # creating a new combined file

combine_18 = sat18.join(act18, on="state") # Joing sat18 and act18, by using index 'state'
combine_18.to_csv('../Classes_clone/projects1234/project_1/data/combine_2018.csv', index = None, header=True) # creating a new combined file

#final = combine_17.join(combine_18, on="state") # Joing combine_17 and combine_18, by using index 'state', but not sure why error
final = pd.merge(combine_17, combine_18, on='state', how='outer') # using merge instead of join seems to work
final.to_csv('../Classes_clone/projects1234/project_1/data/final.csv', index = None, header=True) # creating a new combined file

#print(final.describe().T)

def std_dev(col):
    var = []
    for x in col:
        var.append((1/len(col) * np.power((x - np.mean(col)), 2)))
    sig = np.sqrt(sum(var))
    return sig

#std_dev(final.iloc[:,2])
#print(final.columns[1:])

sd = {y: std_dev(final[y]) for y in final.columns[1:]}
#print(sd)

#print(sat17.sort_values(["participation_s17"], ascending=[False]).head())
#print(sat17.sort_values(["participation_s17"], ascending=[False]).tail())
#print(sat18.sort_values(["participation_s18"], ascending=[False]).head())
#print(sat18.sort_values(["participation_s18"], ascending=[False]).tail())
#print(act17.sort_values(["participation_a17"], ascending=[False]).head())
#print(act17.sort_values(["participation_a17"], ascending=[False]).tail())
#print(act18.sort_values(["participation_a18"], ascending=[False]).head())
#print(act18.sort_values(["participation_a18"], ascending=[False]).tail())

#print(final[(final['participation_s17'] == 1) & (final['participation_s18'] < 1)]) # Do any states with 100% participation on a given test have a rate change year-to-year?
#print(final[(final['participation_a17'] == 1) & (final['participation_a18'] < 1)]) # Do any states with 100% participation on a given test have a rate change y
#print(final[(final['participation_s17'] > 0.5) & (final['participation_a17'] < 0.5)]) # Do any states show have >50% participation on both tests either year?
#print(final[(final['participation_s18'] > 0.5) & (final['participation_a18'] < 0.5)]) # Do any states show have >50% participation on both tests either year?

def corr_heatmap(df):
    plt.figure(figsize=(15, 10))

    # Compute the correlation matrix
    corr = df.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    # Plot our correlation heatmap, while masking the upper triangle to be white.
    sns.axes_style("white")
    sns.heatmap(corr, vmax=2, annot=True, square=True, mask=mask, center=0.0, cmap="YlGnBu")

    # Adding x and y labels
    plt.xlabel("columns")
    plt.ylabel("columns")

    plt.show()


def subplot_histograms(list_of_columns, list_of_titles, list_of_ylabel, list_of_xlabel, dataframe=final):
    nrows = int(np.ceil(len(list_of_columns)/2)) # Makes sure you have enough rows
    fig, ax = plt.subplots(nrows=nrows, ncols=2, figsize=(15, 10)) # You'll want to specify your figsize
    ax = ax.ravel() # Ravel turns a matrix into a vector, which is easier to iterate
    for i, column in enumerate(list_of_columns): # Gives us an index value to get into all our lists
        ax[i].hist(dataframe[column], color="g", alpha=0.5) # feel free to add more settings
        ax[i].set_title(list_of_titles[i])
        ax[i].set_ylabel(list_of_ylabel[i])
        ax[i].set_xlabel(list_of_xlabel[i])
        # Set titles, labels, etc here for each subplot
    plt.show()

print(final.columns)

# Histogram for participation rates
list_of_columns_partn = ["participation_s17", "participation_s18", "participation_a17", "participation_a18"]
list_of_titles_partn = ["participation_s17", "participation_s18", "participation_a17", "participation_a18"]
list_of_ylabel_partn = ["Number of participation", "Number of participation", "Number of participation",
                        "Number of participation"
                        ]
list_of_xlabel_partn = ["Participation", "Participation", "Participation", "Participation"]

# Histogram for math scores
list_of_columns_math = ["math_s17", "math_s18", "math_a17", "math_a18"]
list_of_titles_math = ["math_s17", "math_s18", "math_a17", "math_a18"]
list_of_ylabel_math = ["Number per math scores", "Number per math scores", "Number per math scores",
                       "Number per math scores"
                       ]
list_of_xlabel_math = ["Math scores", "Math scores", "Math scores", "Math scores"]

# Histogram for reading/verbal scores
list_of_columns_read = ["erw_s17", "erw_s18", "readg_a17", "readg_a18"]
list_of_titles_read = ["erw_s17", "erw_s18", "readg_a17", "readg_a18"]
list_of_ylabel_read = ["Number per verbal/reading scores", "Number per verbal/reading scores",
                       "Number per verbal/reading scores",
                       "Number per verbal/reading scores"
                       ]
list_of_xlabel_read = ["verbal/reading scores", "verbal/reading scores", "verbal/reading scores", "verbal/reading scores"]

#subplot_histograms(list_of_columns_read, list_of_titles_read, list_of_ylabel_read, list_of_xlabel_read)

def subplot_scatter(list_of_columns, list_of_rows, list_of_titles, list_of_ylabel, list_of_xlabel, dataframe=final):
    nrows = int(np.ceil(len(list_of_columns)/2)) # Makes sure you have enough rows
    fig, ax = plt.subplots(nrows=nrows, ncols=2, figsize=(15, 20)) # You'll want to specify your figsize
    plt.subplots_adjust(wspace=0.2, hspace=0.5)
    ax = ax.ravel() # Ravel turns a matrix into a vector, which is easier to iterate
    for i, (column, row) in enumerate(zip(list_of_columns, list_of_rows)): # Gives us an index value to get into all our lists
        ax[i].scatter(dataframe[column], dataframe[row], color="g", alpha=0.5) # feel free to add more settings
        ax[i].set_title(list_of_titles[i])
        ax[i].set_ylabel(list_of_ylabel[i])
        ax[i].set_xlabel(list_of_xlabel[i])
        # Set titles, labels, etc here for each subplot
    plt.show()

# Scatter list
list_of_rows_scatter = ['math_s17', 'erw_s17', 'total_s17', 'total_s17', 'composite_a17']
list_of_columns_scatter = ['math_a17', 'readg_a17', 'composite_a17', 'total_s18', 'composite_a18']
list_of_titles_scatter = ["Math scores  SAT 17 vs ACT 17",
                          "Verbal/reading scores  SAT 17 vs ACT 17",
                          "Total SAT 17 vs Composite ACT 17",
                          "Total SAT 17 vs Total SAT 18",
                          "Composite ACT 17 vs Composite ACT 18"
                          ]
list_of_ylabel_scatter = ["Math ACT 2017",
                          "Verbal ACT 2017",
                          "Composite ACT 2017",
                          "Total SAT 2018",
                          "Composite ACT 2017"
                          ]
list_of_xlabel_scatter = ["Math SAT 2017",
                          "ERW SAT 2017",
                          "Total SAT 2017",
                          "Total SAT 2017",
                          "Composite ACT 2018"
                          ]
subplot_scatter(list_of_columns_scatter, list_of_rows_scatter, list_of_titles_scatter, list_of_ylabel_scatter,
                list_of_xlabel_scatter
                )

def subplot_boxplot(list_of_rows, list_of_titles=None, list_of_ylabel=None, list_of_xlabel=None, dataframe=final):
    nrows = int(np.ceil(len(list_of_rows)/2)) # Makes sure you have enough rows
    fig, ax = plt.subplots(nrows=nrows, ncols=2, figsize=(15, 10)) # You'll want to specify your figsize
    ax = ax.ravel() # Ravel turns a matrix into a vector, which is easier to iterate
    #for i, row in enumerate(list_of_rows): # Gives us an index value to get into all our lists
        #print(i, type(row))
    sns.boxplot(data=dataframe[boxplot_participation], ax=ax[0], color="g", width=0.5, palette="colorblind") # feel free to add more settings
    sns.boxplot(data=dataframe[boxplot_ACT17_ACT18], ax=ax[1], color="g", width=0.5,
                palette="colorblind")  # feel free to add more settings
    ax[0].set_title("Participation rate")
    ax[1].set_title("ACT 2017 and 2018 Scores")
    plt.show()

boxplot_participation = ["participation_s17", "participation_s18", "participation_a17", "participation_a18"]
boxplot_ACT17_ACT18 = ["eng_a17", "eng_a18", "math_a17", "math_a18", "readg_a17", "readg_a18", "science_a17",
                       "science_a18"
                       ]
boxplot_ACT17_ACT18_comp = ["composite_a17", "composite_a18"
                            ]
boxplot_SAT17_SAT18_total = ["total_s17", "total_s18"
                             ]
boxplot_SAT17_SAT18 = ["math_s17", "math_s18", "erw_s17", "erw_s18"
                             ]

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 10))
sns.boxplot(data=final, width=0.5, palette="colorblind")
plt.show()

#subplot_boxplot(boxplot_participation)