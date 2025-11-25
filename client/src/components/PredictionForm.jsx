import { useState } from 'react';

function PredictionForm({ onSubmit, isLoading }) {
  const [formData, setFormData] = useState({
    pregnancies: '',
    glucose: '',
    blood_pressure: '',
    skin_thickness: '',
    insulin: '',
    bmi: '',
    diabetes_pedigree_function: '',
    age: ''
  });

  const [errors, setErrors] = useState({});
  const [normalIndex, setNormalIndex] = useState(0);
  const [aboveNormalIndex, setAboveNormalIndex] = useState(0);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const validate = () => {
    const newErrors = {};
    const ranges = {
      pregnancies: { min: 0, max: 20 },
      glucose: { min: 0, max: 500 },
      blood_pressure: { min: 0, max: 200 },
      skin_thickness: { min: 0, max: 100 },
      insulin: { min: 0, max: 1000 },
      bmi: { min: 0, max: 100 },
      diabetes_pedigree_function: { min: 0, max: 5 },
      age: { min: 0, max: 150 }
    };

    Object.keys(formData).forEach(key => {
      const value = formData[key].trim();
      
      if (!value) {
        newErrors[key] = 'This field is required';
        return;
      }

      const numValue = parseFloat(value);
      if (isNaN(numValue)) {
        newErrors[key] = 'Must be a valid number';
        return;
      }

      const range = ranges[key];
      if (numValue < range.min || numValue > range.max) {
        newErrors[key] = `Must be between ${range.min} and ${range.max}`;
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!validate()) {
      return;
    }

    // Convert string values to numbers
    const numericData = {};
    Object.keys(formData).forEach(key => {
      numericData[key] = parseFloat(formData[key]);
    });

    onSubmit(numericData);
  };

  const fieldLabels = {
    pregnancies: 'Pregnancies',
    glucose: 'Glucose (mg/dL)',
    blood_pressure: 'Blood Pressure (mm Hg)',
    skin_thickness: 'Skin Thickness (mm)',
    insulin: 'Insulin (mu U/ml)',
    bmi: 'BMI (kg/m²)',
    diabetes_pedigree_function: 'Diabetes Pedigree Function',
    age: 'Age (years)'
  };

  // Multiple normal/healthy sample data sets
  const normalSamples = [
    {
      pregnancies: '1',
      glucose: '85',
      blood_pressure: '72',
      skin_thickness: '20',
      insulin: '80',
      bmi: '24.5',
      diabetes_pedigree_function: '0.35',
      age: '30'
    },
    {
      pregnancies: '0',
      glucose: '92',
      blood_pressure: '75',
      skin_thickness: '22',
      insulin: '95',
      bmi: '22.8',
      diabetes_pedigree_function: '0.28',
      age: '25'
    },
    {
      pregnancies: '2',
      glucose: '88',
      blood_pressure: '70',
      skin_thickness: '18',
      insulin: '70',
      bmi: '23.2',
      diabetes_pedigree_function: '0.32',
      age: '28'
    },
    {
      pregnancies: '0',
      glucose: '95',
      blood_pressure: '78',
      skin_thickness: '25',
      insulin: '100',
      bmi: '25.1',
      diabetes_pedigree_function: '0.40',
      age: '35'
    },
    {
      pregnancies: '1',
      glucose: '90',
      blood_pressure: '74',
      skin_thickness: '21',
      insulin: '85',
      bmi: '24.0',
      diabetes_pedigree_function: '0.30',
      age: '32'
    }
  ];

  // Multiple above normal/higher risk sample data sets
  const aboveNormalSamples = [
    {
      pregnancies: '3',
      glucose: '155',
      blood_pressure: '88',
      skin_thickness: '35',
      insulin: '200',
      bmi: '32.5',
      diabetes_pedigree_function: '0.85',
      age: '45'
    },
    {
      pregnancies: '5',
      glucose: '168',
      blood_pressure: '92',
      skin_thickness: '40',
      insulin: '250',
      bmi: '35.2',
      diabetes_pedigree_function: '1.05',
      age: '50'
    },
    {
      pregnancies: '2',
      glucose: '142',
      blood_pressure: '85',
      skin_thickness: '32',
      insulin: '180',
      bmi: '30.8',
      diabetes_pedigree_function: '0.72',
      age: '42'
    },
    {
      pregnancies: '4',
      glucose: '175',
      blood_pressure: '95',
      skin_thickness: '38',
      insulin: '280',
      bmi: '38.5',
      diabetes_pedigree_function: '1.15',
      age: '48'
    },
    {
      pregnancies: '1',
      glucose: '148',
      blood_pressure: '82',
      skin_thickness: '30',
      insulin: '165',
      bmi: '29.5',
      diabetes_pedigree_function: '0.68',
      age: '38'
    },
    {
      pregnancies: '6',
      glucose: '185',
      blood_pressure: '98',
      skin_thickness: '42',
      insulin: '320',
      bmi: '40.2',
      diabetes_pedigree_function: '1.25',
      age: '55'
    }
  ];

  const generateDemoData = (type) => {
    if (type === 'normal') {
      const currentSample = normalSamples[normalIndex];
      setFormData(currentSample);
      setNormalIndex((prev) => (prev + 1) % normalSamples.length);
    } else {
      const currentSample = aboveNormalSamples[aboveNormalIndex];
      setFormData(currentSample);
      setAboveNormalIndex((prev) => (prev + 1) % aboveNormalSamples.length);
    }
    // Clear any errors when demo data is loaded
    setErrors({});
  };

  return (
    <form onSubmit={handleSubmit} className="prediction-form">
      <div className="form-header">
        <h2>Enter Health Information</h2>
        <div className="demo-buttons">
          <button
            type="button"
            className="demo-button"
            onClick={() => generateDemoData('normal')}
            disabled={isLoading}
            title={`Fill with normal health values (Sample ${normalIndex + 1}/${normalSamples.length})`}
          >
            Normal
          </button>
          <button
            type="button"
            className="demo-button demo-button-above"
            onClick={() => generateDemoData('above')}
            disabled={isLoading}
            title={`Fill with above normal health values (Sample ${aboveNormalIndex + 1}/${aboveNormalSamples.length})`}
          >
            Above Normal
          </button>
        </div>
      </div>
      <p className="form-description">
        Please provide the following health metrics for diabetes prediction:
      </p>
      
      <div className="form-grid">
        {Object.keys(formData).map((fieldName) => (
          <div key={fieldName} className="form-group">
            <label htmlFor={fieldName}>
              {fieldLabels[fieldName]}
            </label>
            <input
              type="number"
              id={fieldName}
              name={fieldName}
              value={formData[fieldName]}
              onChange={handleChange}
              step={fieldName === 'bmi' || fieldName === 'diabetes_pedigree_function' ? '0.01' : '1'}
              min="0"
              className={errors[fieldName] ? 'error' : ''}
              disabled={isLoading}
            />
            {errors[fieldName] && (
              <span className="error-message">{errors[fieldName]}</span>
            )}
          </div>
        ))}
      </div>

      <button 
        type="submit" 
        className="submit-button"
        disabled={isLoading}
      >
        {isLoading ? 'Predicting...' : 'Predict Diabetes Risk'}
      </button>
    </form>
  );
}

export default PredictionForm;

