import { Employees } from "./employees-model";
import { Patients } from "./patients-model";
import { TypeAppointment } from "./type-appointment-model";

export interface MedicalRecords{
    id: number;
    idPatient: number;
    description: string;
    idEmployees: number;
    dateCreated: Date;
    idTypeAppointment: number;
    patient: Patients;
    employee: Employees;
    typeAppointment: TypeAppointment;

    patientName: string;
    employeeName: string;
    nameAppointment: string;
}