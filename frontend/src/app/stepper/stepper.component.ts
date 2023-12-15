import { Component, OnInit, ElementRef } from '@angular/core';
import { Router } from '@angular/router';
import {CommonModule} from "@angular/common";
import {HttpClient, HttpClientModule} from "@angular/common/http";

@Component({
  selector: 'app-stepper',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './stepper.component.html',
  styleUrl: './stepper.component.css'
})
export class StepperComponent implements OnInit {
  algorithms = [
    { name: 'Algorithm 1', description: 'Description of Algorithm 1' },
    { name: 'Algorithm 2', description: 'Description of Algorithm 2' },
    { name: 'Algorithm 3', description: 'Description of Algorithm 3' },
  ];

  pricingmodels = [
    { name: 'Pricing model 1', description: 'Description of Pricing model 1' },
    { name: 'Pricing model 2', description: 'Description of Pricing model 2' },
    { name: 'Pricing model 3', description: 'Description of Pricing model 3' },
  ];

  twinworlds = [
    { name: 'Twin world 1', description: 'Description of Twin world 1' },
    { name: 'Twin world 2', description: 'Description of Twin world 2' },
    { name: 'Twin world 3', description: 'Description of Twin world 3' },
  ];

  activeStep: number = 1;
  currentDescription: string = '';
  pinnedDescription: string | null = null;

  selectedAlgorithms: any[] = [];
  selectedPricingModels: any[] = [];
  selectedTwinWorlds: any[] = [];

  constructor(private elementRef: ElementRef, private http: HttpClient, private router: Router) { }

  ngOnInit(): void {
    this.elementRef.nativeElement.ownerDocument.body.style.backgroundColor = '#1e1e2d';
  }

  setActiveStep(step: number): void {
    this.activeStep = step;
    this.resetDescriptions();
  }

  getLineProgressWidth(): string {
    switch (this.activeStep) {
      case 1: return '12%';
      case 2: return '52%';
      case 3: return '100%';
      default: return '0%';
    }
  }

  pinDescription(description: string, step: number) {
    this.pinnedDescription = description;
    this.currentDescription = description;

    if (step < 3) {
      this.setActiveStep(step + 1);
    } else {
      this.navigateToSchedulableLoad();
    }
  }

  private navigateToSchedulableLoad() {
    this.router.navigate(['/sl']);
  }

  changeDescription(description: string) {
      this.currentDescription = description;
  }

  resetDescriptions() {
    this.currentDescription = '';
  }

  onAlgorithmSelected(algorithm: any) {
    this.selectedAlgorithms.push(algorithm);
  }

  onPricingModelSelected(model: any) {
    this.selectedPricingModels.push(model);
  }

  onTwinWorldSelected(world: any) {
    this.selectedTwinWorlds.push(world);
  }

  completeSelection() {
    const payload = {
      algorithms: this.selectedAlgorithms,
      pricingModels: this.selectedPricingModels,
      twinWorlds: this.selectedTwinWorlds
    };

    this.http.post('http://localhost:8000/api/simulate/save', payload).subscribe(() => {
      this.navigateToSchedulableLoad();
    });
  }
}
