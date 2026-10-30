'use strict';

function timingReport(durations, budget) {
  if (!Array.isArray(durations) || durations.some(value => !Number.isFinite(value) || value < 0)) {
    throw new Error('durations must be an array of finite nonnegative seconds');
  }
  if (!Number.isFinite(budget) || budget < 0) throw new Error('budget must be finite nonnegative seconds');
  const totalSeconds = durations.reduce((total, value) => total + value, 0);
  if (!Number.isFinite(totalSeconds)) throw new Error('total duration overflow');
  return { count: durations.length, totalSeconds, withinBudget: totalSeconds <= budget };
}

module.exports = { timingReport };
