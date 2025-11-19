// src/app/dashboard/artist/page.tsx
"use client"
import Section from "@/components/layout/Section"
import { RequestForm } from "@/components/forms/RequestForm"
// import { ArtistChart } from "@/components/charts/ArtistChart"

export default function ArtistDashboard() {
  return (
    <main className="min-h-screen bg-neutral-950 text-white p-10 space-y-6">
      <h1 className="text-3xl font-bold">Painel do Tatuador</h1>

      <Section title="Minhas Solicitações">
        <RequestForm />
      </Section>

      <Section title="Metas e Produção">
        {/* <ArtistChart /> */}
      </Section>
    </main>
  )
}
