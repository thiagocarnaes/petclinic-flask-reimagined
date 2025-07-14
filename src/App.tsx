import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Layout } from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import Owners from "./pages/Owners";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <Router>
        <Routes>
          <Route path="/admin" element={<Layout><Dashboard /></Layout>} />
          <Route path="/admin/owners" element={<Layout><Owners /></Layout>} />
          <Route path="/admin/pets" element={<Layout><div>Pets - Coming Soon</div></Layout>} />
          <Route path="/admin/visits" element={<Layout><div>Visits - Coming Soon</div></Layout>} />
          <Route path="/admin/vets" element={<Layout><div>Veterinarians - Coming Soon</div></Layout>} />
          <Route path="/admin/specialties" element={<Layout><div>Specialties - Coming Soon</div></Layout>} />
          <Route path="/admin/pet-types" element={<Layout><div>Pet Types - Coming Soon</div></Layout>} />
          <Route path="/" element={<Index />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Router>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
