// vitest.config.ts
import {defineConfig} from 'vitest/config'

export default defineConfig({
  test: {
    coverage: {
      include: ['src'],
      exclude: ['**/*/index.ts', '**/*/*.d.ts', '**/*/*.test.ts', '**/*/*.tsx']
    },
  },
  define: {
    __CURRENT_URI__: JSON.stringify('http://localhost')
  }
})
