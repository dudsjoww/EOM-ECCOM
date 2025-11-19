"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { motion } from "framer-motion"

export default function AdminDashboard() {
  const [search, setSearch] = useState("")

  const artists = [
    { id: 1, name: "Soyve", specialty: "CyberTattoo", shift: "Noite" },
    { id: 2, name: "Mendes", specialty: "Minimalista", shift: "Dia" },
  ]

  const clients = [
    { id: 1, name: "Cliente 1", email: "cliente1@email.com" },
    { id: 2, name: "Cliente 2", email: "cliente2@email.com" },
  ]

  return (
    <section className="min-h-screen bg-neutral-950 text-white p-10 space-y-10">
      {/* TÍTULO */}
      <motion.h1
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-3xl font-bold"
      >
        Painel Administrativo
      </motion.h1>

      {/* PESQUISA */}
      <div className="max-w-md">
        <Input
          placeholder="Buscar artista, cliente ou sessão..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* ARTISTAS */}
      <section>
        <h2 className="text-xl font-semibold mb-4">Tatuadores</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {artists.map((a) => (
            <motion.div
              key={a.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-zinc-800 rounded-xl p-4 border border-zinc-700"
            >
              <h3 className="text-lg font-semibold">{a.name}</h3>
              <p className="text-sm text-gray-400">{a.specialty}</p>
              <p className="text-sm text-gray-400">Turno: {a.shift}</p>
              <Button className="mt-3 w-full bg-red-600 hover:bg-red-700">
                Gerenciar
              </Button>
            </motion.div>
          ))}
        </div>
      </section>

      {/* CLIENTES */}
      <section>
        <h2 className="text-xl font-semibold mb-4">Clientes</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {clients.map((c) => (
            <motion.div
              key={c.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-zinc-800 rounded-xl p-4 border border-zinc-700"
            >
              <h3 className="text-lg font-semibold">{c.name}</h3>
              <p className="text-sm text-gray-400">{c.email}</p>
              <Button className="mt-3 w-full bg-red-600 hover:bg-red-700">
                Detalhes
              </Button>
            </motion.div>
          ))}
        </div>
      </section>

      {/* SESSÕES */}
      <section>
        <h2 className="text-xl font-semibold mb-4">Sessões / Solicitações</h2>
        <div className="bg-zinc-800 rounded-xl p-6 border border-zinc-700">
          <p className="text-gray-400">
            Em breve: controle de agendamentos e solicitações.
          </p>
        </div>
      </section>
    </section>
  )
}
