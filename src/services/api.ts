const API_BASE_URL = 'http://localhost:5000/api';

// API Client
class ApiClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    const response = await fetch(url, config);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response.json();
  }

  // Generic CRUD operations
  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint);
  }

  async post<T>(endpoint: string, data: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async put<T>(endpoint: string, data: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'DELETE',
    });
  }
}

export const apiClient = new ApiClient(API_BASE_URL);

// Type definitions
export interface Owner {
  id?: number;
  first_name: string;
  last_name: string;
  address: string;
  city: string;
  telephone: string;
  created_at?: string;
  updated_at?: string;
}

export interface PetType {
  id?: number;
  name: string;
  created_at?: string;
  updated_at?: string;
}

export interface Pet {
  id?: number;
  name: string;
  birth_date: string;
  owner_id: number;
  type_id: number;
  created_at?: string;
  updated_at?: string;
  owner?: Owner;
  type?: PetType;
}

export interface Specialty {
  id?: number;
  name: string;
  created_at?: string;
  updated_at?: string;
}

export interface Vet {
  id?: number;
  first_name: string;
  last_name: string;
  specialties?: Specialty[];
  created_at?: string;
  updated_at?: string;
}

export interface Visit {
  id?: number;
  visit_date: string;
  description: string;
  pet_id: number;
  created_at?: string;
  updated_at?: string;
  pet?: Pet;
}

export interface PaginatedResponse<T> {
  data: T[];
  page: number;
  per_page: number;
  total: number;
  pages: number;
}

// API Services
export const ownerService = {
  getAll: (page = 1, per_page = 10) => 
    apiClient.get<PaginatedResponse<Owner>>(`/owners?page=${page}&per_page=${per_page}`),
  getById: (id: number) => 
    apiClient.get<Owner>(`/owners/${id}`),
  create: (data: Omit<Owner, 'id'>) => 
    apiClient.post<Owner>('/owners', data),
  update: (id: number, data: Partial<Owner>) => 
    apiClient.put<Owner>(`/owners/${id}`, data),
  delete: (id: number) => 
    apiClient.delete(`/owners/${id}`),
};

export const petService = {
  getAll: (page = 1, per_page = 10) => 
    apiClient.get<PaginatedResponse<Pet>>(`/pets?page=${page}&per_page=${per_page}`),
  getById: (id: number) => 
    apiClient.get<Pet>(`/pets/${id}`),
  create: (data: Omit<Pet, 'id'>) => 
    apiClient.post<Pet>('/pets', data),
  update: (id: number, data: Partial<Pet>) => 
    apiClient.put<Pet>(`/pets/${id}`, data),
  delete: (id: number) => 
    apiClient.delete(`/pets/${id}`),
};

export const visitService = {
  getAll: (page = 1, per_page = 10) => 
    apiClient.get<PaginatedResponse<Visit>>(`/visits?page=${page}&per_page=${per_page}`),
  getById: (id: number) => 
    apiClient.get<Visit>(`/visits/${id}`),
  create: (data: Omit<Visit, 'id'>) => 
    apiClient.post<Visit>('/visits', data),
  update: (id: number, data: Partial<Visit>) => 
    apiClient.put<Visit>(`/visits/${id}`, data),
  delete: (id: number) => 
    apiClient.delete(`/visits/${id}`),
};

export const vetService = {
  getAll: (page = 1, per_page = 10) => 
    apiClient.get<PaginatedResponse<Vet>>(`/vets?page=${page}&per_page=${per_page}`),
  getById: (id: number) => 
    apiClient.get<Vet>(`/vets/${id}`),
  create: (data: Omit<Vet, 'id'>) => 
    apiClient.post<Vet>('/vets', data),
  update: (id: number, data: Partial<Vet>) => 
    apiClient.put<Vet>(`/vets/${id}`, data),
  delete: (id: number) => 
    apiClient.delete(`/vets/${id}`),
};

export const specialtyService = {
  getAll: (page = 1, per_page = 10) => 
    apiClient.get<PaginatedResponse<Specialty>>(`/specialties?page=${page}&per_page=${per_page}`),
  getById: (id: number) => 
    apiClient.get<Specialty>(`/specialties/${id}`),
  create: (data: Omit<Specialty, 'id'>) => 
    apiClient.post<Specialty>('/specialties', data),
  update: (id: number, data: Partial<Specialty>) => 
    apiClient.put<Specialty>(`/specialties/${id}`, data),
  delete: (id: number) => 
    apiClient.delete(`/specialties/${id}`),
};

export const petTypeService = {
  getAll: (page = 1, per_page = 10) => 
    apiClient.get<PaginatedResponse<PetType>>(`/pet-types?page=${page}&per_page=${per_page}`),
  getById: (id: number) => 
    apiClient.get<PetType>(`/pet-types/${id}`),
  create: (data: Omit<PetType, 'id'>) => 
    apiClient.post<PetType>('/pet-types', data),
  update: (id: number, data: Partial<PetType>) => 
    apiClient.put<PetType>(`/pet-types/${id}`, data),
  delete: (id: number) => 
    apiClient.delete(`/pet-types/${id}`),
};