function standardise(unitData) {
    unitData.sort((a, b) => (a.unitCode > b.unitCode) ? 1 : -1)

    const unitCount = unitData.length;

    const initial = {
        assessment: 0,
        feedback: 0,
        satisfaction: 0,
        resources: 0,
        activities: 0
    }

    const dataSum = unitData.reduce((prev, current) => {
        return {
            assessment: prev.assessment + current.assessment,
            feedback: prev.feedback + current.feedback,
            satisfaction:  prev.satisfaction + current.satisfaction,
            resources: prev.resources + current.resources,
            activities: prev.resources + current.resources
        }
    }, initial)

    const dataAverage = {
        assessment: dataSum.assessment / unitCount,
        feedback: dataSum.feedback / unitCount,
        satisfaction: dataSum.satisfaction / unitCount,
        resources: dataSum.resources / unitCount,
        activities: dataSum.activities / unitCount
    }

    const dataVariance = unitData.reduce((prev, current) => {
        return {
            assessment: prev.assessment + (current.assessment - Math.pow(dataAverage.assessment, 2)),
            feedback: prev.feedback + (current.feedback - Math.pow(dataAverage.feedback, 2)),
            satisfaction: prev.satisfaction + (current.satisfaction - Math.pow(dataAverage.satisfaction, 2)),
            resources: prev.resources + (current.resources - Math.pow(dataAverage.resources, 2)),
            activities: prev.activities + (current.activities - Math.pow(dataAverage.activities, 2)),
        }
    }, initial);

    const standardScores = unitData.map(e => {
        return {
            assessment: ((e.assessment - dataAverage.assessment) / Math.sqrt(dataVariance.assessment)) + 3,
            feedback: ((e.feedback - dataAverage.feedback) / Math.sqrt(dataVariance.feedback)) + 3,
            satisfaction: ((e.satisfaction - dataAverage.satisfaction) / Math.sqrt(dataVariance.satisfaction)) + 3,
            resources: ((e.resources - dataAverage.resources) / Math.sqrt(dataVariance.resources)) + 3,
            activities: ((e.activities - dataAverage.activities) / Math.sqrt(dataVariance.activities)) + 3,
        }
    });

    return standardScores;  
}
