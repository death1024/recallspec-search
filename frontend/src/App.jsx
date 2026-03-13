import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'
import IdentitySpec from './components/IdentitySpec'
import ActionCard from './components/ActionCard'

function App() {
  const [query, setQuery] = useState('')
  const [image, setImage] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [searchMode, setSearchMode] = useState('text')

  const handleSearch = async () => {
    setLoading(true)
    try {
      const response = await axios.post('/api/v1/search', { query })
      setResult(response.data)
    } catch (error) {
      console.error('Search failed:', error)
    }
    setLoading(false)
  }

  const handleImageSearch = async () => {
    if (!image) return
    setLoading(true)
    try {
      const formData = new FormData()
      formData.append('image', image)
      if (query) formData.append('query', query)

      const response = await axios.post('/api/v1/search/image', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setResult(response.data)
    } catch (error) {
      console.error('Image search failed:', error)
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8 text-white"
        >
          <h1 className="text-5xl font-bold mb-3">🔍 RecallSpec Search</h1>
          <p className="text-xl opacity-90">AI-Powered Product Recall Verification</p>
        </motion.div>

        {/* Search Card */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-white/95 backdrop-blur-lg rounded-2xl shadow-2xl p-6 md:p-8 mb-6"
        >
          {/* Search Mode Tabs */}
          <div className="flex gap-3 mb-6">
            {['text', 'image', 'barcode'].map((mode) => (
              <button
                key={mode}
                onClick={() => setSearchMode(mode)}
                className={`flex-1 py-3 px-4 rounded-xl font-semibold transition-all ${
                  searchMode === mode
                    ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {mode === 'text' && '📝 Text'}
                {mode === 'image' && '📷 Image'}
                {mode === 'barcode' && '🔢 VIN/UPC'}
              </button>
            ))}
          </div>

          <AnimatePresence mode="wait">
            {searchMode === 'text' && (
              <motion.div
                key="text"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
              >
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Enter product name, brand, or description..."
                  className="w-full px-6 py-4 text-lg border-2 border-gray-200 rounded-xl focus:border-indigo-500 focus:outline-none transition-colors"
                />
              </motion.div>
            )}

            {searchMode === 'image' && (
              <motion.div
                key="image"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-indigo-400 transition-colors cursor-pointer"
                onClick={() => document.getElementById('file-input').click()}
              >
                <input
                  id="file-input"
                  type="file"
                  accept="image/*"
                  onChange={(e) => setImage(e.target.files[0])}
                  className="hidden"
                />
                <p className="text-lg text-gray-600">
                  📷 {image ? image.name : 'Click to upload product image'}
                </p>
              </motion.div>
            )}

            {searchMode === 'barcode' && (
              <motion.div
                key="barcode"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
              >
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Enter VIN or UPC code..."
                  className="w-full px-6 py-4 text-lg border-2 border-gray-200 rounded-xl focus:border-indigo-500 focus:outline-none transition-colors font-mono"
                />
              </motion.div>
            )}
          </AnimatePresence>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={searchMode === 'image' ? handleImageSearch : handleSearch}
            disabled={loading}
            className="w-full mt-6 py-4 bg-gradient-to-r from-indigo-500 to-purple-500 text-white text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all disabled:opacity-50"
          >
            {loading ? '⏳ Searching...' : '🔎 Search for Recalls'}
          </motion.button>
        </motion.div>

        {/* Loading State */}
        <AnimatePresence>
          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="bg-white/95 backdrop-blur-lg rounded-2xl shadow-2xl p-8 text-center"
            >
              <div className="inline-block w-16 h-16 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mb-4" />
              <p className="text-gray-600 text-lg">Analyzing product and checking recall databases...</p>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Results */}
        <AnimatePresence>
          {result && !loading && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              <IdentitySpec spec={result.identity_spec} />
              <ActionCard
                actionCard={result.resolution_spec?.action_card}
                riskLevel={result.resolution_spec?.risk_level}
                matchStatus={result.resolution_spec?.match_status}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}

export default App
