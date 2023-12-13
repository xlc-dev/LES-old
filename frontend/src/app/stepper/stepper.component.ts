import {Component, ElementRef, OnInit, AfterViewInit} from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-stepper',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './stepper.component.html',
  styleUrl: './stepper.component.css'
})
export class StepperComponent implements OnInit, AfterViewInit {
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

  currentDescription: string = '';
  pinnedDescription: string | null = null;

  selectedAlgorithm: any = null;
  selectedPricingModel: any = null;
  selectedTwinWorld: any = null;

  constructor(private elementRef: ElementRef) { }

  ngOnInit(): void {

  }

  changeDescription(description: string) {
    if (this.pinnedDescription === null) {
      this.currentDescription = description;
    }
  }

  pinDescription(description: string) {
    this.pinnedDescription = description;
    this.currentDescription = description;
  }

  resetDescriptions() {
    this.currentDescription = '';
    this.pinnedDescription = null;
  }

  ngAfterViewInit() {
    const self = this;

    this.elementRef.nativeElement.ownerDocument
      .body.style.backgroundColor = '#1e1e2d';

    $(".step").click(function() {
      $(this).addClass("active").prevAll().addClass("active");
      $(this).nextAll().removeClass("active");
      self.resetDescriptions();
    });

    $(".step01").click(function() {
      $("#line-progress").css("width", "12%");
      $(".step1").addClass("active").siblings().removeClass("active");
    });

    $(".step02").click(function() {
      $("#line-progress").css("width", "52%");
      $(".step2").addClass("active").siblings().removeClass("active");
    });

    $(".step03").click(function() {
      $("#line-progress").css("width", "100%");
      $(".step3").addClass("active").siblings().removeClass("active");
    });
  }
}
