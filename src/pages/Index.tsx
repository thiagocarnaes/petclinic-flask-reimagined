import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Heart, Users, Calendar, UserCheck } from "lucide-react";

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Welcome to PetClinic
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
            Professional veterinary management system
          </p>
          
          <Link to="/admin">
            <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
              Access Admin Panel
            </Button>
          </Link>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
          <Card className="text-center">
            <CardHeader>
              <Users className="h-12 w-12 text-blue-600 mx-auto mb-4" />
              <CardTitle>Pet Owners</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                Manage pet owner information and contact details
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="text-center">
            <CardHeader>
              <Heart className="h-12 w-12 text-pink-600 mx-auto mb-4" />
              <CardTitle>Pets</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                Keep track of all pets and their medical records
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="text-center">
            <CardHeader>
              <Calendar className="h-12 w-12 text-green-600 mx-auto mb-4" />
              <CardTitle>Visits</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                Schedule and manage veterinary appointments
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="text-center">
            <CardHeader>
              <UserCheck className="h-12 w-12 text-purple-600 mx-auto mb-4" />
              <CardTitle>Veterinarians</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                Manage veterinary staff and their specialties
              </CardDescription>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Index;
