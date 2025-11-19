"use client"
import { useState } from "react"
import { Menu, User } from "lucide-react"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <header className="w-full bg-black text-white shadow-lg border-b border-red-700">
      <div className="max-w-7xl mx-auto flex justify-between items-center px-6 py-4">
        {/* LOGO */}
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-red-600 rounded-full" />
          <span className="font-bold text-lg tracking-wide">INK Master</span>
        </div>

        {/* MENU */}
        <nav className="hidden md:flex items-center gap-6">
          <a href="#" className="hover:text-red-500 transition">Início</a>
          <Link href="{#sectionArtist}">
            <p className="hover:text-red-500 transition">Artistas</p>
          </Link>
          <a href="#" className="hover:text-red-500 transition">Agendamentos</a>
          <a href="#" className="hover:text-red-500 transition">Contato</a>
        </nav>

        {/* PERFIL */}
        <div className="relative">
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="flex items-center gap-2 bg-red-700 px-3 py-2 rounded-lg hover:bg-red-800 transition"
          >
            <User size={18} />
            <span className="hidden sm:block">Perfil</span>
          </button>

          {menuOpen && (
            <div className="absolute right-0 mt-2 w-40 bg-zinc-900 border border-zinc-700 rounded-lg shadow-lg z-10">
              <a
                href="#"
                className="block px-4 py-2 text-sm hover:bg-red-600 transition"
              >
                Configurações
              </a>
              <a
                href="#"
                className="block px-4 py-2 text-sm hover:bg-red-600 transition"
              >
                Sair
              </a>
            </div>
          )}
        </div>

        {/* MENU MOBILE */}
        <div className="md:hidden">
          <Button
            variant="outline"
            size="sm"
            className="text-white border-zinc-700 hover:bg-red-700"
            onClick={() => setMenuOpen(!menuOpen)}
          >
            <Menu size={20} />
          </Button>
        </div>
      </div>

      {/* MENU MOBILE ABERTO */}
      {menuOpen && (
        <div className="md:hidden bg-zinc-900 border-t border-zinc-800">
          <nav className="flex flex-col px-6 py-3 gap-2">
            <a href="#" className="hover:text-red-500 transition">Início</a>
            <a href="#" className="hover:text-red-500 transition">Artistas</a>
            <a href="#" className="hover:text-red-500 transition">Agendamentos</a>
            <a href="#" className="hover:text-red-500 transition">Contato</a>
          </nav>
        </div>
      )}
    </header>
  )
}
