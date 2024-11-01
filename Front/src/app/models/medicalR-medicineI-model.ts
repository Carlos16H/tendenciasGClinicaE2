import { MedicalRecords } from "./medical-records-model";
import { MedicineInventory } from "./medicine-inventory-model";

export interface MedicalRMedicineI{
    id: number;
    idMedicalRecords: number;
    idMedicineInventory: number;
    amount: number;
    medicalRecords: MedicalRecords;
    medicineInventory: MedicineInventory;
}