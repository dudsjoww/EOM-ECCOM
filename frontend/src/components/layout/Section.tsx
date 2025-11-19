// src/components/layout/Section.tsx
import { motion } from "framer-motion"

export default function Section({ title, children }: any) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="bg-zinc-900 rounded-2xl p-6 my-4 border border-zinc-800"
    >
      {title && <h2 className="text-xl font-semibold mb-4">{title}</h2>}
      {children}
    </motion.section>
  )
}
