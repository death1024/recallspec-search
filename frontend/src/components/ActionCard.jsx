import { motion } from 'framer-motion'

export default function ActionCard({ actionCard, riskLevel, matchStatus }) {
  if (!actionCard) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white/95 backdrop-blur-lg rounded-2xl shadow-2xl p-6 md:p-8"
      >
        <div className="text-center py-8">
          <div className="text-6xl mb-4">✅</div>
          <h3 className="text-2xl font-bold text-gray-800 mb-2">No Recalls Found</h3>
          <p className="text-gray-600">This product has no active recalls in our database.</p>
        </div>
      </motion.div>
    )
  }

  const riskConfig = {
    high: {
      border: 'border-red-500',
      bg: 'bg-red-50',
      text: 'text-red-700',
      icon: '🚨'
    },
    medium: {
      border: 'border-orange-500',
      bg: 'bg-orange-50',
      text: 'text-orange-700',
      icon: '⚠️'
    },
    low: {
      border: 'border-green-500',
      bg: 'bg-green-50',
      text: 'text-green-700',
      icon: 'ℹ️'
    },
    unknown: {
      border: 'border-gray-500',
      bg: 'bg-gray-50',
      text: 'text-gray-700',
      icon: '❓'
    }
  }

  const config = riskConfig[riskLevel] || riskConfig.unknown

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`${config.bg} border-4 ${config.border} rounded-2xl shadow-2xl p-6 md:p-8`}
    >
      <div className="flex items-center gap-3 mb-6">
        <span className="text-4xl">{config.icon}</span>
        <div>
          <h3 className={`text-2xl font-bold ${config.text}`}>
            Recall Alert - {riskLevel.toUpperCase()} Risk
          </h3>
          <p className="text-sm text-gray-600 mt-1">
            Match Status: {matchStatus?.replace('_', ' ').toUpperCase()}
          </p>
        </div>
      </div>

      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.2 }}
        className={`bg-white border-l-4 ${config.border} rounded-xl p-5 mb-6 shadow-md`}
      >
        <p className="text-lg font-semibold text-gray-800">
          {actionCard.immediate_action}
        </p>
      </motion.div>

      <h4 className="text-lg font-bold text-gray-800 mb-4">📋 Next Steps:</h4>
      <ol className="space-y-3 ml-6 list-decimal">
        {actionCard.next_steps?.map((step, i) => (
          <motion.li
            key={i}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 + i * 0.1 }}
            className="text-gray-700 leading-relaxed"
          >
            {step}
          </motion.li>
        ))}
      </ol>

      {actionCard.official_source && (
        <motion.a
          href={actionCard.official_source}
          target="_blank"
          rel="noopener noreferrer"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="mt-6 block bg-white rounded-xl p-4 shadow-md hover:shadow-lg transition-shadow"
        >
          <span className="text-indigo-600 font-semibold">
            📄 View Official Source →
          </span>
        </motion.a>
      )}
    </motion.div>
  )
}
