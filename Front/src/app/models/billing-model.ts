import { MedicalRecords } from "./medical-records-model";
import { Patients } from "./patients-model";

export interface Billing{
    id: number;
    idPatients: number;
    idMedicalRecords: number;
    date: Date;
    totalAmount: number;
    details: string;
    paymentStatus: string;
    patient: Patients;
    medicalRecords: MedicalRecords;

    patientName: string;
    dateMedicalRecords: Date;
    typeAppointment: string;
    documentPatient: string;
}