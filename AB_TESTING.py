#####################################################
# Comparison of AB testing with Conversation of Bidding methods
#####################################################

#####################################################
# Task 1:  Preparing and analysing the data
#####################################################

# Reading file and assigning variables as control and test group df.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, levene, ttest_ind, mannwhitneyu

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.7f' % x)
pd.set_option('display.width', 500)
control_group = pd.read_excel("ab_testing.xlsx", usecols=[0, 1, 2, 3], sheet_name="Control Group")
test_group = pd.read_excel("ab_testing.xlsx", usecols=[0, 1, 2, 3], sheet_name="Test Group")

# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.
control_group.head()
control_group.shape == test_group.shape
control_group["bidding"] = "max"
test_group["bidding"] = "avg"

# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

df = pd.concat([control_group, test_group], ignore_index=True)
df["purchase_per_click"] = df["Purchase"] / df["Click"]
df[df["bidding"] == "max"].describe().T
df[df["bidding"] == "avg"].describe().T

#####################################################
# Describing the hypotesis of A/B testing
#####################################################

# H0: M1 = M2   (there is no difference between purchase_per_click of control and test groups  )
# H1: M1 != M2  (there is difference between purchase_per_click of control and test groups)

# Analysing the avg purchase per click values for control and test groups
df.groupby("bidding").agg({"purchase_per_click": "mean"})
df.groupby("bidding").agg({"Earning": "mean"})
######################################################
# AB Testing of two independent variables
######################################################



# Before hypotesis test, normality assumption and variance homojenity need to be checked
# H0: normally distributed
# H1: not normally distributed
'''both p-values are less than 0.05, does not fıt normality assumption. H0 is rejected'''

test_stat, pvalue = shapiro(df.loc[df["bidding"] == "max", "purchase_per_click"])  # Test St = 0.8720, p-value = 0.0003
df[df["bidding"] == "avg"].describe().T

test_stat, pvalue = shapiro(df.loc[df["bidding"] == "avg", "purchase_per_click"])  # Test St = 0.8381, p-value = 0.0000

# H0: variance is homogeneus
# H1: variance is not homogeneus
'''p-value greater than 0.05, the variance is homogeneus. H0 can't be rejected'''

test_stat, pvalue = levene(df.loc[df["bidding"] == "max", "purchase_per_click"],
                           df.loc[df["bidding"] == "avg", "purchase_per_click"])  # Test St = 2.0759, p-value = 0.1536
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# As normality assumption was disproven I will conduct non-parametric test

test_stat, pvalue = mannwhitneyu(df.loc[df["bidding"] == "max", "purchase_per_click"],
                              df.loc[df["bidding"] == "avg", "purchase_per_click"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))  # Test Stat = 459.0000, p-value = 0.0011
##############################################################
# Analysing the results
##############################################################

# the test to prove normality distribution of variables was shapiro which is most powerful method
# As have non-normal distribution, Levene was used to prove variance homogenity
# As we have non-normal distribution, non-parametric test was conducted


# the statistical analyze shows that customers are inclined to make more purchase when they see
# average bidding

