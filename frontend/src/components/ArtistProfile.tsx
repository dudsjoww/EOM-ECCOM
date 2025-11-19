"use client"

import Image from "next/image"
import { Button } from "@/components/ui/button"
import { motion } from "framer-motion"
import Footer from "@/components/layout/footer"
import Contact from "@/components/layout/footer"
import Header from "@/components/layout/header"

export default function ArtistProfile({ artist }: any) {
  return (
    <section className="min-h-screen bg-zinc-900 text-white flex flex-col items-center py-10">
      <Header />
      {/* HERO */}
      <div className="grid grid-cols-2 gap-4 w-full max-w-5xl">
        {artist.heroImages.map((img: string, idx: number) => (
          <motion.div
            key={idx}

            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.2 }}
            className="flex flex-col items-center justify-center bg-zinc-800 rounded-2xl p-8"
          >
            <Image
              src={img}
              alt={`Hero ${idx + 1}`}
              width={200}
              height={200}
              className="rounded-full border border-gray-600"
            />
            <p className="mt-4 text-sm text-gray-300">
              IMG {idx + 1} HERO
            </p>
          </motion.div>
        ))}
      </div>

      {/* SOBRE */}
      <div className="bg-red-600 w-full max-w-5xl my-10 rounded-xl p-10 text-center flex flex-col items-center justify-center">
        <h2 className="text-lg font-bold mb-2">About Me:</h2>
        <p className="text-white text-md">{artist.bio}</p>
      </div>

      {/* ÍCONES / ESPECIALIDADES */}
      <div className="flex gap-10 mb-10 text-center">
        <div>
          <p className="font-semibold">{artist.specialty}</p>
          <p className="text-gray-400 text-sm">Especialidade</p>
        </div>
        <div>
          <p className="font-semibold">{artist.favoriteTheme}</p>
          <p className="text-gray-400 text-sm">Adora</p>
        </div>
        <div>
          <p className="font-semibold">{artist.workShift}</p>
          <p className="text-gray-400 text-sm">Turno</p>
        </div>
      </div>

      {/* CONTATO */}
      <div className="grid grid-cols-2 gap-6 max-w-4xl w-full">
        <div>
          <h3 className="font-semibold mb-2">Deixe seu email ou contato</h3>
          <input
            type="email"
            placeholder="email@example"
            className="w-full p-2 rounded-md text-black"
          />
        </div>

        <div>
          <Contact />
          <h3 className="font-semibold mb-2">Mensagem</h3>
          <textarea
            rows={3}
            placeholder="Mensagem..."
            className="w-full p-2 rounded-md text-black"
          />
        </div>
      </div>

      <Button className="mt-8">Enviar Mensagem</Button>
    </section>


  )
}
