"use client"

import { useState } from "react"
import { motion } from "framer-motion"

export default function Contact() {
  const [email, setEmail] = useState("")
  const [mensagem, setMensagem] =
    useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log({ email, mensagem })
    // Aqui você vai futuramente enviar os dados ao backend Python (FastAPI)
    setEmail("")
    setMensagem("")
  }

  return (
    <motion.section
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7 }}
      viewport={{ once: true }}
      className="max-w-5xl mx-auto px-6 text-center"
    >
      <h2 className="text-3xl font-semibold mb-8">Deixe seu email ou contato</h2>

      <form
        onSubmit={handleSubmit}
        className="grid grid-cols-1 md:grid-cols-2 gap-8 text-left"
      >
        {/* Campo de email */}
        <div className="flex flex-col">
          <label htmlFor="email" className="mb-2 text-gray-300">
            Email:
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="email@example.com"
            className="bg-neutral-800 text-white rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-red-500"
            required
          />
        </div>

        {/* Campo de mensagem */}
        <div className="flex flex-col">
          <label htmlFor="mensagem" className="mb-2 text-gray-300">
            Mensagem:
          </label>
          <textarea
            id="mensagem"
            value={mensagem}
            onChange={(e) => setMensagem(e.target.value)}
            placeholder="Digite sua mensagem..."
            className="bg-neutral-800 text-white rounded-lg px-4 py-3 h-32 resize-none focus:outline-none focus:ring-2 focus:ring-red-500"
            required
          />
        </div>

        {/* Botão de envio */}
        <div className="col-span-1 md:col-span-2 flex justify-center mt-6">
          <button
            type="submit"
            className="bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-full transition"
          >
            Enviar
          </button>
        </div>
      </form>
    </motion.section>
  )
}
