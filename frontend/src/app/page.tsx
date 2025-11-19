"use client"

import { motion } from "framer-motion"
import Hero from "@/components/hero"
import Artists from "@/components/artists"
import Features from "@/components/features"
import Contact from "@/components/layout/footer"
import { Button } from "@/components/ui/button"
import Header from "@/components/layout/header"

export default function Home() {
const artist = [
    { id: 1, name: "Rafael Mendes" },
    { id: 2, name: "Marcos Silva" },
  ]

  return (
    <main className="bg-neutral-800 text-white">
      <Header />
      {/* Seção inicial */}
      <section className="relative">
        <Hero />
      </section>

      {/* About us */}
      <section className="bg-gradient-to-b from-neutral-900 to-neutral-800 text-center py-24 px-6">
        <motion.h2
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-4xl font-semibold mb-6"
        >
          Sobre nós
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3, duration: 0.8 }}
          className="text-gray-300 max-w-2xl mx-auto"
        >
          Nosso estúdio é um espaço dedicado à arte, precisão e autenticidade. 
          Cada tatuagem é um projeto único, criado em parceria com você para expressar sua identidade.
        </motion.p>
      </section>

      {/* Artistas */}
      <section className="bg-neutral-100 text-black ">
        <Artists />
      </section>

    

      {/* Features */}
      <section className="bg-neutral-200 text-black">
        <Features />
      </section>

      {/* Call to Action */}
      <section className="bg-neutral-900 text-center py-24">
        <motion.h3
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-2xl font-semibold mb-6"
        >
          Registre-se e agende uma tatuagem conosco
        </motion.h3>

        <Button className="bg-gray-100 text-black hover:bg-gray-200 rounded-full px-6 py-3">
          Cadastre-se
        </Button>
      </section>

      {/* Contato */}
      <section className="bg-neutral-950 py-24">
        <Contact />
      </section>
    </main>
  )
}
