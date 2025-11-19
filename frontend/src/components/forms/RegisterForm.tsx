"use client"
import { useRouter } from "next/navigation"
import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export default function LoginForm() {
  const router = useRouter()
  const [role, setRole] = useState("client") // mock até autenticação

  const handleLogin = () => {
    router.push(`/dashboard/${role}`)
  }

  return (
    <div className="bg-red-700 text-white p-6 rounded-2xl w-[300px] flex flex-col gap-3">
      <Input placeholder="Email" type="email" />
      <Input placeholder="Senha" type="password" />
      <select
        className="bg-red-600 text-white rounded-md p-2 mt-2"
        value={role}
        onChange={(e) => setRole(e.target.value)}
      >
        <option value="client">Cliente</option>
        <option value="artist">Tatuador</option>
        <option value="admin">Admin</option>
      </select>
      <Button onClick={handleLogin} className="mt-3">Entrar</Button>
    </div>
  )
}
