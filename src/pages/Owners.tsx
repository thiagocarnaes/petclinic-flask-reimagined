import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Plus, Edit, Trash2, Search } from "lucide-react";
import { ownerService, Owner, PaginatedResponse } from "@/services/api";
import { useToast } from "@/hooks/use-toast";

const ownerSchema = z.object({
  first_name: z.string().min(1, "First name is required").max(30, "First name too long"),
  last_name: z.string().min(1, "Last name is required").max(30, "Last name too long"),
  address: z.string().min(1, "Address is required").max(255, "Address too long"),
  city: z.string().min(1, "City is required").max(80, "City too long"),
  telephone: z.string().min(1, "Telephone is required").max(20, "Telephone too long"),
});

type OwnerFormData = z.infer<typeof ownerSchema>;

export default function Owners() {
  const [owners, setOwners] = useState<Owner[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingOwner, setEditingOwner] = useState<Owner | null>(null);
  const { toast } = useToast();

  const form = useForm<OwnerFormData>({
    resolver: zodResolver(ownerSchema),
    defaultValues: {
      first_name: "",
      last_name: "",
      address: "",
      city: "",
      telephone: "",
    },
  });

  const fetchOwners = async (page = 1) => {
    try {
      setLoading(true);
      const response: PaginatedResponse<Owner> = await ownerService.getAll(page, 10);
      setOwners(response.data);
      setCurrentPage(response.page);
      setTotalPages(response.pages);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch owners",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOwners();
  }, []);

  const handleSubmit = async (data: OwnerFormData) => {
    try {
      if (editingOwner) {
        await ownerService.update(editingOwner.id!, data as Owner);
        toast({
          title: "Success",
          description: "Owner updated successfully",
        });
      } else {
        await ownerService.create(data as Owner);
        toast({
          title: "Success",
          description: "Owner created successfully",
        });
      }
      
      setIsDialogOpen(false);
      setEditingOwner(null);
      form.reset();
      fetchOwners(currentPage);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to save owner",
        variant: "destructive",
      });
    }
  };

  const handleEdit = (owner: Owner) => {
    setEditingOwner(owner);
    form.reset({
      first_name: owner.first_name,
      last_name: owner.last_name,
      address: owner.address,
      city: owner.city,
      telephone: owner.telephone,
    });
    setIsDialogOpen(true);
  };

  const handleDelete = async (id: number) => {
    if (confirm("Are you sure you want to delete this owner?")) {
      try {
        await ownerService.delete(id);
        toast({
          title: "Success",
          description: "Owner deleted successfully",
        });
        fetchOwners(currentPage);
      } catch (error) {
        toast({
          title: "Error",
          description: "Failed to delete owner",
          variant: "destructive",
        });
      }
    }
  };

  const filteredOwners = owners.filter(owner => 
    `${owner.first_name} ${owner.last_name}`.toLowerCase().includes(searchTerm.toLowerCase()) ||
    owner.city.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Owners</h2>
          <p className="text-muted-foreground">Manage pet owners</p>
        </div>
        
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button onClick={() => {
              setEditingOwner(null);
              form.reset();
            }}>
              <Plus className="mr-2 h-4 w-4" />
              Add Owner
            </Button>
          </DialogTrigger>
          
          <DialogContent className="sm:max-w-[425px]">
            <DialogHeader>
              <DialogTitle>
                {editingOwner ? "Edit Owner" : "Add New Owner"}
              </DialogTitle>
              <DialogDescription>
                {editingOwner ? "Update owner information" : "Enter owner details below"}
              </DialogDescription>
            </DialogHeader>
            
            <Form {...form}>
              <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
                <FormField
                  control={form.control}
                  name="first_name"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>First Name</FormLabel>
                      <FormControl>
                        <Input {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                
                <FormField
                  control={form.control}
                  name="last_name"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Last Name</FormLabel>
                      <FormControl>
                        <Input {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                
                <FormField
                  control={form.control}
                  name="address"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Address</FormLabel>
                      <FormControl>
                        <Input {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                
                <FormField
                  control={form.control}
                  name="city"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>City</FormLabel>
                      <FormControl>
                        <Input {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                
                <FormField
                  control={form.control}
                  name="telephone"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Telephone</FormLabel>
                      <FormControl>
                        <Input {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                
                <div className="flex justify-end space-x-2">
                  <Button 
                    type="button" 
                    variant="outline"
                    onClick={() => setIsDialogOpen(false)}
                  >
                    Cancel
                  </Button>
                  <Button type="submit">
                    {editingOwner ? "Update" : "Create"}
                  </Button>
                </div>
              </form>
            </Form>
          </DialogContent>
        </Dialog>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Owners List</CardTitle>
          <CardDescription>
            All registered pet owners in the system
          </CardDescription>
          
          <div className="flex items-center space-x-2">
            <Search className="h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search owners..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="max-w-sm"
            />
          </div>
        </CardHeader>
        
        <CardContent>
          {loading ? (
            <div className="text-center py-4">Loading...</div>
          ) : (
            <div className="space-y-4">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Address</TableHead>
                    <TableHead>City</TableHead>
                    <TableHead>Phone</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredOwners.map((owner) => (
                    <TableRow key={owner.id}>
                      <TableCell className="font-medium">
                        {owner.first_name} {owner.last_name}
                      </TableCell>
                      <TableCell>{owner.address}</TableCell>
                      <TableCell>{owner.city}</TableCell>
                      <TableCell>{owner.telephone}</TableCell>
                      <TableCell className="text-right">
                        <div className="flex justify-end space-x-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleEdit(owner)}
                          >
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleDelete(owner.id!)}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
              
              {filteredOwners.length === 0 && !loading && (
                <div className="text-center py-4 text-muted-foreground">
                  No owners found
                </div>
              )}
              
              <div className="flex items-center justify-between">
                <div className="text-sm text-muted-foreground">
                  Page {currentPage} of {totalPages}
                </div>
                <div className="space-x-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => fetchOwners(currentPage - 1)}
                    disabled={currentPage <= 1}
                  >
                    Previous
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => fetchOwners(currentPage + 1)}
                    disabled={currentPage >= totalPages}
                  >
                    Next
                  </Button>
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}