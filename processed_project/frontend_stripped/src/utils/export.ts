export function exportToCSV(data:Record<string,any>[],filename:string):void{if(!data||!data.length){console.warn('No data to export');return;}const headers=Object.keys(data[0]);const csvRows=[];csvRows.push(headers.join(','));for(const row of data){const values=headers.map(header=>{const value=row[header]||'';const escaped=String(value).replace(/"/g, '""');
      return `"${escaped}"`;
    });
    csvRows.push(values.join(__STRING_5__));
  }

  
  const csvContent = csvRows.join(__STRING_6__);

  
  const blob = new Blob([csvContent], { type: __STRING_7__ });
  const url = URL.createObjectURL(blob);

  
  const link = document.createElement(__STRING_8__);
  link.setAttribute(__STRING_9__, url);
  link.setAttribute(__STRING_10__, `${filename}.csv`);link.style.visibility='hidden';document.body.appendChild(link);link.click();document.body.removeChild(link);}