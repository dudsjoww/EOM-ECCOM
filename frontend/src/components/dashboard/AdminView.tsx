// src/app/dashboard/admin/page.tsx
"use client"
import Section from "@/components/layout/Section"
import { RequestForm } from "@/components/forms/RequestForm"
// import { StudioChart } from "@/components/charts/StudioChart"

export default function AdminDashboard() {
  return (
    <main className="min-h-screen bg-neutral-950 text-white p-10 space-y-6">
      <h1 className="text-3xl font-bold">Painel do Gestor / Admin</h1>

      <Section title="Solicitações Gerais">
        <RequestForm readOnly />
      </Section>

      <Section title="Estatísticas do Estúdio">
        {/* <StudioChart /> */}
      </Section>


          <div className="p-6">
      <h2 className="text-xl font-bold mb-4">Visão Geral</h2>
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-gray-100 p-4 rounded-lg">Clientes: 120</div>
        <div className="bg-gray-100 p-4 rounded-lg">Tatuadores: 12</div>
        <div className="bg-gray-100 p-4 rounded-lg">Vendas: R$ 48.000</div>
      </div>
    </div>
    </main>
  )
}
