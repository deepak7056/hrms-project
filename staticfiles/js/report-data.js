// report-data.js - Handles report data management

// Function to convert Excel decimal time to readable format
function convertExcelTime(excelTime) {
  if (!excelTime || isNaN(excelTime)) return excelTime;
  
  const totalMinutes = Math.round(excelTime * 24 * 60);
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  
  const period = hours >= 12 ? 'PM' : 'AM';
  const displayHours = hours > 12 ? hours - 12 : (hours === 0 ? 12 : hours);
  
  return `${displayHours}:${minutes.toString().padStart(2, '0')} ${period}`;
}

// Load Excel file from server
async function loadExcelFromServer() {
  try {
    console.log('Starting to load Excel file...');
    
    const response = await fetch('Report_list.xlsx');
    console.log('Response status:', response.status);
    
    if (!response.ok) {
      throw new Error(`File not found! Status: ${response.status}`);
    }
    
    const arrayBuffer = await response.arrayBuffer();
    console.log('File loaded successfully, size:', arrayBuffer.byteLength);
    
    // Parse Excel file
    const workbook = XLSX.read(arrayBuffer, { type: 'array' });
    console.log('Workbook parsed, sheets:', workbook.SheetNames);
    
    const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
    const jsonData = XLSX.utils.sheet_to_json(firstSheet);
    console.log('Data extracted, rows:', jsonData.length);
    
    // Process and store data
    const reportsWithIds = jsonData.map((report, index) => {
      // Convert time fields if they are decimal numbers
      Object.keys(report).forEach(key => {
        if (key === 'PublishTime' && typeof report[key] === 'number') {
          report[key] = convertExcelTime(report[key]);
        }
      });
      
      return {
        id: Date.now() + index,
        ...report
      };
    });
    
    const headers = Object.keys(jsonData[0] || {});
    
    localStorage.setItem('allReports', JSON.stringify(reportsWithIds));
    localStorage.setItem('reportHeaders', JSON.stringify(headers));
    
    console.log('Data stored successfully!');
    
    // Refresh the display
    if (window.displayReports) {
      window.displayReports();
    }
  } catch (error) {
    console.error('Error loading Excel file:', error);
    
    // Load sample data as fallback
    console.log('Loading sample data instead...');
    loadSampleData();
  }
}

// Sample data fallback
function loadSampleData() {
  const sampleData = [
    {
      "S.No": 1,
      "ID": 12,
      "ReportName": "Forecast Accuracy Dashboard",
      "Days": "Monthly",
      "ReportStatus": "Active",
      "WhoseRequireThisReport": "Abhishek Anand",
      "BaseInputFile": "BQ",
      "ActuleTime": 90,
      "PublishTime": "10:00 AM",
      "ReportType": "Planning"
    },
    {
      "S.No": 2,
      "ID": 13,
      "ReportName": "Forecast Accuracy - Reason Codes",
      "Days": "Monthly",
      "ReportStatus": "Active",
      "WhoseRequireThisReport": "Abhishek Anand",
      "BaseInputFile": "BQ",
      "ActuleTime": 90,
      "PublishTime": "10:00 AM",
      "ReportType": "Planning"
    }
  ];
  
  const reportsWithIds = sampleData.map((report, index) => ({
    id: Date.now() + index,
    ...report
  }));
  
  const headers = Object.keys(sampleData[0]);
  
  localStorage.setItem('allReports', JSON.stringify(reportsWithIds));
  localStorage.setItem('reportHeaders', JSON.stringify(headers));
  
  if (window.displayReports) {
    window.displayReports();
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
  // Clear any old data first
  localStorage.removeItem('allReports');
  localStorage.removeItem('reportHeaders');
  
  // Then load fresh data
  loadExcelFromServer();
});

// Export all functions properly
window.reportDataUtils = {
  loadExcelFromServer: loadExcelFromServer,
  convertExcelTime: convertExcelTime,
  loadSampleData: loadSampleData
};