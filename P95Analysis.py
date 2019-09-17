import matplotlib.pyplot as plt
import numpy as np

# Gets a normal distribution with a minimum
from matplotlib import mlab


def getNumbersFromCappedNormalDistribution(median, stdev, minimum, count, cacheHitRate, cacheGetSetDurationDuration):
    accumulatedFilteredNumbers = []
    while True:
        numbers = np.random.normal(median, stdev, count - len(accumulatedFilteredNumbers))
        filteredNumbers = list(filter(lambda n: n > minimum, numbers))
        accumulatedFilteredNumbers.extend(filteredNumbers)
        if len(accumulatedFilteredNumbers) == count:
            break
    # now, we iterate and apply the cache hit rate
    for i in range(len(accumulatedFilteredNumbers)):
        number = accumulatedFilteredNumbers[i]
        cacheDuration = max(0.1, np.random.normal(cacheGetSetDurationDuration, cacheGetSetDurationDuration * 2))
        if np.random.random() < cacheHitRate:
            # cache hit
            number = max(0.1, cacheDuration)
        else:
            number = number + cacheDuration
        accumulatedFilteredNumbers[i] = number
    return accumulatedFilteredNumbers

# Add 2 arrays
def add2Arrays(list1, list2):
    resultArray = []
    for i in range(0, len(list1)):
        resultArray.append(list1[i] + list2[i])
    return resultArray

def showHistogram(list, title):
    count, bins, ignored = plt.hist(list, 30, density=True, label='Load time')  # Make a histogram
    plt.title(title)
    plt.xlabel('Duration', y=1.08)
    plt.ylabel('Distribution density')
    plt.xlim(0, 12)
    plt.ylim(0, 0.7)
    # Percentile values
    p = np.array([0.0, 25.0, 50.0, 75.0, 95.0, 99.0])
    sortedDurations = np.sort(list)
    percentiles = np.percentile(sortedDurations, p)
    for i in range(0, len(p)):
        plt.text(8, 0.5 - i * 0.08, 'P' + str(int(p[i])) + ':' + str(round(percentiles[i], 1)), fontsize=12,
                 fontweight='bold')
    plt.show(block=False)

def runSampleWithoutCaching():
    numSamples = 100000
    durationsForApiCall1 = getNumbersFromCappedNormalDistribution(2, 1, 0.5, numSamples, 0, 0)
    plt.subplot(221)
    showHistogram(durationsForApiCall1, 'API call 1')

    durationsForApiCall2 = getNumbersFromCappedNormalDistribution(2, 1.3, 0.4, numSamples, 0, 0)
    plt.subplot(222)
    showHistogram(durationsForApiCall2, 'API call 2')

    durationsForApiCall3 = getNumbersFromCappedNormalDistribution(1, 0.7, 0.3, numSamples, 0, 0)
    plt.subplot(223)
    showHistogram(durationsForApiCall3, 'API call 3')

    totalDuration = add2Arrays(add2Arrays(durationsForApiCall1, durationsForApiCall2), durationsForApiCall3)
    plt.subplot(224)
    showHistogram(totalDuration, 'Total')
    plt.show()

def runSampleWithCaching():
    numSamples = 100000
    durationsForApiCall1 = getNumbersFromCappedNormalDistribution(2, 1, 0.5, numSamples, 0.3, 0.2)
    plt.subplot(221)
    showHistogram(durationsForApiCall1, 'API call 1 (with caching)')

    durationsForApiCall2 = getNumbersFromCappedNormalDistribution(2, 1.3, 0.4, numSamples, 0.3, 0.2)
    plt.subplot(222)
    showHistogram(durationsForApiCall2, 'API call 2 (with caching)')

    durationsForApiCall3 = getNumbersFromCappedNormalDistribution(1, 0.7, 0.3, numSamples, 0.3, 0.2)
    plt.subplot(223)
    showHistogram(durationsForApiCall3, 'API call 3 (with caching)')

    totalDuration = add2Arrays(add2Arrays(durationsForApiCall1, durationsForApiCall2), durationsForApiCall3)
    plt.subplot(224)
    showHistogram(totalDuration, 'Total (with caching)')
    plt.show()

np.random.seed(10298301) # Make re-runs constant
runSampleWithoutCaching()
runSampleWithCaching()