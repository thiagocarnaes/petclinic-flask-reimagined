import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Users, Heart, Calendar, UserCheck } from "lucide-react";
import { ownerService, petService, visitService, vetService } from "@/services/api";

interface DashboardStats {
  owners: number;
  pets: number;
  visits: number;
  vets: number;
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats>({
    owners: 0,
    pets: 0,
    visits: 0,
    vets: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [ownersData, petsData, visitsData, vetsData] = await Promise.all([
          ownerService.getAll(1, 1),
          petService.getAll(1, 1),
          visitService.getAll(1, 1),
          vetService.getAll(1, 1),
        ]);

        setStats({
          owners: ownersData.total,
          pets: petsData.total,
          visits: visitsData.total,
          vets: vetsData.total,
        });
      } catch (error) {
        console.error('Error fetching dashboard stats:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  const statCards = [
    {
      title: "Total Owners",
      value: stats.owners,
      description: "Registered pet owners",
      icon: Users,
      color: "text-blue-600",
    },
    {
      title: "Total Pets",
      value: stats.pets,
      description: "Pets under care",
      icon: Heart,
      color: "text-pink-600",
    },
    {
      title: "Total Visits",
      value: stats.visits,
      description: "Veterinary visits",
      icon: Calendar,
      color: "text-green-600",
    },
    {
      title: "Total Veterinarians",
      value: stats.vets,
      description: "Active veterinarians",
      icon: UserCheck,
      color: "text-purple-600",
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        <p className="text-muted-foreground">
          Welcome to PetClinic Administration System
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {statCards.map((card) => (
          <Card key={card.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {card.title}
              </CardTitle>
              <card.icon className={`h-4 w-4 ${card.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {loading ? "..." : card.value}
              </div>
              <p className="text-xs text-muted-foreground">
                {card.description}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card className="col-span-2">
          <CardHeader>
            <CardTitle>System Overview</CardTitle>
            <CardDescription>
              PetClinic management system statistics
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center space-x-2">
              <Badge variant="outline">Status</Badge>
              <span className="text-sm text-green-600">System Online</span>
            </div>
            <div className="flex items-center space-x-2">
              <Badge variant="outline">API</Badge>
              <span className="text-sm">Connected to backend</span>
            </div>
            <div className="flex items-center space-x-2">
              <Badge variant="outline">Database</Badge>
              <span className="text-sm">MySQL Active</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>
              Common administrative tasks
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="text-sm space-y-1">
              <p>• Register new owner</p>
              <p>• Add new pet</p>
              <p>• Schedule visit</p>
              <p>• Add veterinarian</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}