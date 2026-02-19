"use client"

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { X } from "lucide-react"
import { TrainingSession, Lap } from "@/lib/data-processor"

interface HREvolutionChartProps {
  session: TrainingSession
  onClose: () => void
}

function getLapSeparators(laps: Lap[]): Array<{ time_seconds: number; lap_number: number }> {
  if (!laps || laps.length === 0) return []

  // Laps con duration_seconds: acumular para obtener tiempo de corte entre laps
  if (laps[0]?.duration_seconds !== undefined) {
    let cumulative = 0
    return laps.slice(0, -1).map((lap, i) => {
      cumulative += lap.duration_seconds!
      return { time_seconds: cumulative, lap_number: i + 1 }
    })
  }

  // Laps con approximate_time_seconds: ya es tiempo absoluto desde inicio
  if (laps[0]?.approximate_time_seconds !== undefined) {
    return laps.map((lap) => ({
      time_seconds: lap.approximate_time_seconds!,
      lap_number: lap.lap_number,
    }))
  }

  return []
}

const HR_MIN_VALID = 30
const HR_MAX_VALID = 250

export function HREvolutionChart({ session, onClose }: HREvolutionChartProps) {
  const validSamples = (session.hr_samples ?? []).filter(
    (s) => s.hr != null && s.hr >= HR_MIN_VALID && s.hr <= HR_MAX_VALID
  )

  const chartData = validSamples.map((s) => ({
    time: s.time_seconds / 60,
    hr: s.hr,
  }))

  const hrValues = validSamples.map((s) => s.hr)
  const minHR = hrValues.length > 0 ? Math.min(...hrValues) : 60
  const maxHR = hrValues.length > 0 ? Math.max(...hrValues) : 180
  const avgHR =
    hrValues.length > 0 ? hrValues.reduce((a, b) => a + b, 0) / hrValues.length : 0

  const yMin = Math.max(30, Math.floor((minHR - 10) / 10) * 10)
  const yMax = Math.ceil((maxHR + 10) / 10) * 10
  const maxTimeMins = chartData.length > 0 ? Math.max(...chartData.map((d) => d.time)) : 0
  const xMax = Math.ceil(maxTimeMins / 5) * 5

  const lapSeparators = getLapSeparators(session.laps ?? [])

  const date = new Date(session.start_time)
  const dateLabel = date.toLocaleDateString("es-ES", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  })

  return (
    <Card className="mt-6 scroll-mt-4" id="hr-evolution-chart">
      <CardHeader>
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <CardTitle className="flex items-center gap-2">
              <span>❤️ Evolución de Frecuencia Cardíaca</span>
            </CardTitle>
            <p className="text-sm text-muted-foreground mt-1 capitalize">{dateLabel}</p>
            <div className="flex flex-wrap gap-x-3 gap-y-1 text-sm text-muted-foreground mt-1">
              <span>⏱ {session.duration_formatted}</span>
              {session.hr_avg && <span>Prom: <strong>{session.hr_avg} bpm</strong></span>}
              {session.hr_max && <span>Máx: <strong>{session.hr_max} bpm</strong></span>}
              {session.hr_min && <span>Mín: <strong>{session.hr_min} bpm</strong></span>}
              <span className="text-muted-foreground/60">{validSamples.length} muestras</span>
            </div>
            {lapSeparators.length > 0 && (
              <div className="flex flex-wrap gap-2 mt-2">
                {lapSeparators.map((lap) => {
                  const mins = Math.floor(lap.time_seconds / 60)
                  const secs = lap.time_seconds % 60
                  return (
                    <span
                      key={lap.lap_number}
                      className="inline-flex items-center gap-1.5 text-xs bg-indigo-50 text-indigo-700 border border-indigo-200 rounded-full px-2.5 py-0.5"
                    >
                      <span className="w-3 border-t-2 border-dashed border-indigo-400 inline-block" />
                      Lap {lap.lap_number} — {mins}:{String(secs).padStart(2, "0")}
                    </span>
                  )
                })}
              </div>
            )}
          </div>
          <Button variant="ghost" size="sm" onClick={onClose} className="shrink-0 -mt-1 -mr-2">
            <X className="w-4 h-4" />
          </Button>
        </div>
      </CardHeader>

      <CardContent>
        {chartData.length === 0 ? (
          <div className="text-center py-12 text-muted-foreground">
            Esta sesión no tiene muestras de frecuencia cardíaca disponibles.
          </div>
        ) : (
          <ResponsiveContainer width="100%" height={360}>
            <LineChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />

              <XAxis
                dataKey="time"
                type="number"
                domain={[0, xMax]}
                tickCount={Math.min(12, Math.floor(xMax / (xMax <= 30 ? 2 : xMax <= 60 ? 5 : 10)) + 1)}
                tickFormatter={(v) => `${v} min`}
                fontSize={11}
                label={{
                  value: "Tiempo (minutos)",
                  position: "insideBottom",
                  offset: -12,
                  fontSize: 12,
                  fill: "hsl(var(--muted-foreground))",
                }}
              />

              <YAxis
                domain={[yMin, yMax]}
                tickFormatter={(v) => `${v}`}
                fontSize={11}
                label={{
                  value: "FC (bpm)",
                  angle: -90,
                  position: "insideLeft",
                  offset: 12,
                  fontSize: 12,
                  fill: "hsl(var(--muted-foreground))",
                }}
              />

              <Tooltip
                formatter={(value: number) => [`${value} bpm`, "FC"]}
                labelFormatter={(val: number) => {
                  const mins = Math.floor(val)
                  const secs = Math.round((val - mins) * 60)
                  return `${mins}:${String(secs).padStart(2, "0")} min`
                }}
                contentStyle={{ fontSize: 13 }}
              />

              {/* Línea de HR promedio */}
              <ReferenceLine
                y={avgHR}
                stroke="hsl(174 72% 45%)"
                strokeDasharray="5 5"
                strokeWidth={1.5}
                label={{
                  value: `Prom ${Math.round(avgHR)} bpm`,
                  position: "insideTopRight",
                  fontSize: 11,
                  fill: "hsl(174 72% 35%)",
                }}
              />

              {/* Separadores de laps */}
              {lapSeparators.map((lap) => {
                const xVal = lap.time_seconds / 60
                if (xVal <= 0 || xVal >= maxTimeMins) return null
                return (
                  <ReferenceLine
                    key={lap.lap_number}
                    x={xVal}
                    stroke="hsl(239 84% 67%)"
                    strokeDasharray="6 3"
                    strokeWidth={2}
                    label={{
                      value: `Lap ${lap.lap_number}`,
                      position: "insideTopLeft",
                      fontSize: 11,
                      fill: "hsl(239 84% 50%)",
                    }}
                  />
                )
              })}

              <Line
                type="monotone"
                dataKey="hr"
                stroke="hsl(0 84.2% 60.2%)"
                strokeWidth={1.5}
                dot={false}
                activeDot={{ r: 4, fill: "hsl(0 84.2% 60.2%)" }}
                isAnimationActive={chartData.length < 500}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </CardContent>
    </Card>
  )
}
