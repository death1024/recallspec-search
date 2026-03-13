import { motion } from 'framer-motion'

export default function IdentitySpec({ spec }) {
  if (!spec) return null

  const statusColors = {
    complete: 'bg-green-500',
    partial: 'bg-orange-500',
    minimal: 'bg-red-500'
  }

  const fields = [
    { key: 'brand', label: 'Brand', value: spec.brand },
    { key: 'model', label: 'Model', value: spec.model },
    { key: 'vin', label: 'VIN', value: spec.vin, mono: true },
    { key: 'upc', label: 'UPC', value: spec.upc, mono: true },
    { key: 'category', label: 'Category', value: spec.category?.replace('_', ' ') }
  ].filter(f => f.value)

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white/95 backdrop-blur-lg rounded-2xl shadow-2xl p-6 md:p-8"
    >
      <div className="flex items-center gap-3 mb-6">
        <h3 className="text-2xl font-bold text-gray-800">Product Identity</h3>
        <span className={`px-3 py-1 ${statusColors[spec.status]} text-white text-sm font-semibold rounded-full uppercase`}>
          {spec.status}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {fields.map((field, i) => (
          <motion.div
            key={field.key}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.1 }}
            className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-4 hover:shadow-md transition-shadow"
          >
            <div className="text-xs text-gray-500 mb-1 uppercase tracking-wide">{field.label}</div>
            <div className={`text-lg font-semibold text-gray-800 ${field.mono ? 'font-mono' : ''}`}>
              {field.value}
            </div>
          </motion.div>
        ))}
      </div>

      {spec.missing_fields?.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-6 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded-lg"
        >
          <span className="font-semibold text-yellow-800">⚠️ Missing:</span>
          <span className="ml-2 text-yellow-700">{spec.missing_fields.join(', ')}</span>
        </motion.div>
      )}
    </motion.div>
  )
}
