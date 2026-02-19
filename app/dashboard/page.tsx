"use client"

import { useEffect, useRef, useState } from "react"
import { useRouter } from "next/navigation"
import { TrainingData, TrainingSession, processTrainingData, groupByMonth, groupDurationByMonth } from "@/lib/data-processor"
import { StatsCards } from "@/components/stats-cards"
import { MonthlySessionsChart } from "@/components/charts/monthly-sessions-chart"
import { HRChart } from "@/components/charts/hr-chart"
import { DurationChart } from "@/components/charts/duration-chart"
import { SessionsList } from "@/components/sessions-list"
import { HREvolutionChart } from "@/components/charts/hr-evolution-chart"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Activity } from "lucide-react"

export default function Dashboard() {
  const router = useRouter()
  const [data, setData] = useState<TrainingData | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedSession, setSelectedSession] = useState<TrainingSession | null>(null)
  const hrChartRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const storedData = localStorage.getItem('trainingData')
    if (!storedData) {
      router.push('/')
      return
    }

    try {
      const parsedData = JSON.parse(storedData) as TrainingData
      setData(parsedData)
    } catch (error) {
      console.error('Error loading data:', error)
      router.push('/')
    } finally {
      setLoading(false)
    }
  }, [router])

  function handleSelectSession(session: TrainingSession) {
    if (!session.has_hr || !session.hr_samples || session.hr_samples.length === 0) return

    // Deseleccionar si se hace clic en la misma sesión
    if (selectedSession?.start_time === session.start_time) {
      setSelectedSession(null)
      return
    }

    setSelectedSession(session)

    // Scroll al gráfico después de renderizar
    setTimeout(() => {
      hrChartRef.current?.scrollIntoView({ behavior: "smooth", block: "start" })
    }, 50)
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-500 via-purple-600 to-indigo-700 flex items-center justify-center">
        <div className="text-white text-xl">Cargando dashboard...</div>
      </div>
    )
  }

  if (!data) {
    return null
  }

  const stats = processTrainingData(data)
  const monthlyData = groupByMonth(data.sessions)
  const durationByMonth = groupDurationByMonth(data.sessions)

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-500 via-purple-600 to-indigo-700">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <Activity className="w-10 h-10 text-white" />
            <div>
              <h1 className="text-3xl md:text-4xl font-bold text-white">
                Dashboard de Entrenamientos
              </h1>
              <p className="text-white/80">
                {data.total_sessions} entrenamientos · Exportado el {new Date(data.export_date).toLocaleDateString('es-ES')}
              </p>
            </div>
          </div>
          <Button 
            variant="outline" 
            onClick={() => router.push('/')}
            className="bg-white/10 text-white border-white/20 hover:bg-white/20"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Volver
          </Button>
        </div>

        {/* Stats Cards */}
        <div className="mb-8">
          <StatsCards stats={stats} />
        </div>

        {/* Charts */}
        <div className="space-y-6 mb-8">
          <MonthlySessionsChart data={monthlyData} />
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <HRChart sessions={data.sessions} />
            <DurationChart data={durationByMonth} />
          </div>
        </div>

        {/* Sessions List */}
        <SessionsList
          sessions={data.sessions}
          selectedSession={selectedSession}
          onSelectSession={handleSelectSession}
        />

        {/* HR Evolution Chart — se muestra al hacer clic en una sesión */}
        {selectedSession && (
          <div ref={hrChartRef}>
            <HREvolutionChart
              session={selectedSession}
              onClose={() => setSelectedSession(null)}
            />
          </div>
        )}
      </div>
    </main>
  )
}
