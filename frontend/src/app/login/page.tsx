"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import LoginForm from "@/components/forms/LoginForm"
import RegisterForm from "@/components/forms/RegisterForm"

export default function LoginPage() {
  const router = useRouter()
  const [role, setRole] = useState("client") // ou 'artist', 'admin'

  const handleLogin = async () => {
    // simulação de login (depois você conecta API ou DB)
    if (role === "client") router.push("/client")
    if (role === "artist") router.push("/artist")
    if (role === "admin") router.push("/admin")
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-neutral-900 text-white">
      <LoginForm />
      {/* <RegisterForm /> */}
    </main>
  )
}
