import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { TrainingSession } from "@/lib/data-processor"
import { Heart, MapPin, Clock } from "lucide-react"

interface SessionsListProps {
  sessions: TrainingSession[]
}

export function SessionsList({ sessions }: SessionsListProps) {
  const sortedSessions = [...sessions].sort(
    (a, b) => new Date(b.start_time).getTime() - new Date(a.start_time).getTime()
  ).slice(0, 15) // Mostrar las últimas 15

  return (
    <Card>
      <CardHeader>
        <CardTitle>Entrenamientos Recientes</CardTitle>
        <CardDescription>Últimas 15 sesiones registradas</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {sortedSessions.map((session, index) => {
            const date = new Date(session.start_time)
            return (
              <div 
                key={session.id || index}
                className="flex flex-col md:flex-row md:items-center justify-between p-4 border rounded-lg hover:bg-muted/50 transition-colors gap-3"
              >
                <div className="flex-1">
                  <div className="font-semibold">
                    {date.toLocaleDateString('es-ES', { 
                      weekday: 'long', 
                      year: 'numeric', 
                      month: 'long', 
                      day: 'numeric' 
                    })}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {date.toLocaleTimeString('es-ES', { 
                      hour: '2-digit', 
                      minute: '2-digit' 
                    })}
                  </div>
                </div>

                <div className="flex items-center gap-2 text-sm">
                  <Clock className="w-4 h-4 text-muted-foreground" />
                  <span>{session.duration_formatted}</span>
                </div>

                <div className="flex flex-wrap gap-2">
                  {session.has_hr && session.hr_avg && (
                    <Badge variant="outline" className="gap-1">
                      <Heart className="w-3 h-3" />
                      {session.hr_avg} bpm
                    </Badge>
                  )}
                  {session.has_gps && session.distance_meters && (
                    <Badge variant="outline" className="gap-1">
                      <MapPin className="w-3 h-3" />
                      {(session.distance_meters / 1000).toFixed(2)} km
                    </Badge>
                  )}
                  {!session.parseable && (
                    <Badge variant="destructive">
                      Datos básicos
                    </Badge>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}
