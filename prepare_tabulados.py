"""python prepare_tabulados.py path/to/Data_Actualizada.xlsx"""
import json,sys,hashlib,datetime,unicodedata,re
from pathlib import Path
import openpyxl
def norm(s):
 s=re.sub(r'^\d{9}\s*','',str(s)).split(',')[0].strip()
 s=''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn')
 return s.replace('gustvo','gustavo')
def build_data(source):
 root=Path(__file__).resolve().parent
 w=openpyxl.load_workbook(source,read_only=True,data_only=True)
 raw={s.title:[list(r) for r in s.values] for s in w}
 specs=[('birth','Pais o entidad nacimiento','CDMX',2,['Localidad','Estimador','Población','En CDMX (%)','Otra entidad (%)','Estados Unidos (%)','Otro país¹ (%)','No especificado² (%)']),('residence','Residencia hace 5 años','CDMX',2,['Localidad','Estimador','Población de 5 años y más','Misma demarcación (%)','Otra demarcación de CDMX (%)','Demarcación no especificada (%)','Otra entidad (%)','Estados Unidos (%)','Otro país¹ (%)','No especificado² (%)']),('populationNational','Poblacion Nacional','Nacional',3,['Entidad','2020','2025','Diferencia absoluta','Variación (fracción)','Estructura (fracción)']),('populationCity','Poblacion Cdmx','CDMX',1,['Alcaldía','Población','Mujeres','Hombres']),('educationNational','Educacion Nacional','Nacional',2,['Concepto','2020','2025','Diferencia absoluta','Variación (%)','Estructura (fracción)']),('educationCity','Educación CDMX','CDMX',2,['Concepto','2020','2025','Diferencia absoluta','Variación (%)','Estructura (fracción)']),('incomeNational','Ingresos Monetarios Nacional','Nacional',2,['Concepto','2020','2025','Diferencia absoluta','Variación (fracción)','Estructura (fracción)']),('incomeCity','Ingresos Monetarios CDMX','CDMX',2,['Concepto','2020','2025','Diferencia absoluta','Variación (fracción)','Estructura (fracción)']),('housingCity','Vivienda por Alcaldía','CDMX',1,['Alcaldía','Cantidad','Estructura (fracción)']),('housingType','Viviendas particulares habitada','CDMX',1,['Concepto','Cantidad','Estructura (fracción)']),('disabilityNational','Discapacidad Nacional','Nacional',1,['Edad','2020','2025']),('disabilityCity','Discapacidad Cdmx','CDMX',1,['Edad','2020']),('healthNational','Salud Nacional','Nacional',2,['Concepto','2020','2025'])]
 tables={}
 for key,sheet,region,start,headers in specs:
  rows=[{'label':str(r[0]).strip(),'key':norm(r[0]),'values':r[1:],'excelRow':i+1} for i,r in enumerate(raw[sheet]) if i>=start and r[0] is not None and len(r)>1 and (isinstance(r[1],(int,float)) or r[1]=='Valor')]
  notes=[str(r[0]) for r in raw[sheet][start:] if r[0] and (str(r[0]).startswith(('Nota:','¹','²','Los límites')))]
  tables[key]={'sheet':sheet,'region':region,'headers':headers,'rows':rows,'notes':notes}
 education_notes=[
  '1/ Población de 3 años y más.',
  '2/ Incluye a la población que tiene al menos un grado aprobado en estudios técnicos o comerciales con primaria terminada.',
  '3/ Incluye a la población que tiene al menos un grado aprobado en estudios técnicos o comerciales con secundaria terminada, preparatoria o bachillerato (general o tecnológico) o normal básica con primaria o secundaria terminada.',
  '4/ Incluye a la población que tiene al menos un grado aprobado en estudios técnicos o comerciales con preparatoria terminada, normal de licenciatura, licenciatura, especialidad, maestría o doctorado.'
 ]
 for key in ['educationCity','educationNational']:
  tables[key]['notes']=education_notes
  tables[key]['notesSource']='Notas complementarias de educación proporcionadas por el usuario.'
 income_notes=[
  '1/ El porcentaje para cada tipo de fuente se obtuvo con respecto al total de hogares. La suma de los porcentajes puede ser mayor a 100%, debido a que un mismo hogar puede recibir ingresos monetarios de más de una fuente distinta al trabajo.',
  '2/ Considera las fuentes de ingresos monetarios que los integrantes del hogar reciben a través de programas sociales del gobierno federal o estatal. Estos incluyen becas para estudiantes, pensiones para adultos mayores o para personas con discapacidad, así como apoyos destinados a jóvenes o a campesinos, entre otros programas.'
 ]
 for key in ['incomeCity','incomeNational']:
  tables[key]['notes']=income_notes
  tables[key]['notesSource']='Notas complementarias de ingresos proporcionadas por el usuario.'
 issues=[]
 for key in ['populationNational','populationCity','housingCity','housingType','disabilityNational','disabilityCity']:
  t=tables[key]; total=t['rows'][0]
  cols=[0,1] if key in ['populationNational','disabilityNational'] else [0]
  for col in cols:
   s=sum(r['values'][col] for r in t['rows'][1:]);v=total['values'][col]
   if abs(s-v)>.1:issues.append({'sheet':t['sheet'],'message':f"{t['headers'][col+1]}: las filas suman {s:,.0f}; el total publicado en la hoja es {v:,.0f}. Diferencia: {s-v:,.0f}."})
 city=tables['populationCity']['rows'];assert len(city)==17
 for r in city:assert abs(r['values'][1]+r['values'][2]-r['values'][0])<.1
 for key in ['birth','residence']:
  assert len(tables[key]['rows'])==15
  for r in tables[key]['rows']:assert abs(sum(r['values'][2:])-100)<.00001
 assert len(tables['populationNational']['rows'])==33
 issues.extend([{'sheet':'Ingresos Monetarios CDMX','message':'La columna Estructura divide entre el total nacional (39,699,242), no entre el total CDMX. Las gráficas usan cantidades; la tabla conserva ese campo original.'},{'sheet':'Discapacidad Cdmx','message':'La única columna de año es 2020. No hay valor 2025 en esta hoja.'},{'sheet':'Salud','message':'Hay llamadas a notas cuyo texto no está incluido. No se infieren universos o exclusividad de categorías.'}])
 d={'source':Path(source).name,'sha256':hashlib.sha256(Path(source).read_bytes()).hexdigest(),'extracted':datetime.date.today().isoformat(),'tables':tables,'issues':issues}
 baseline=json.loads((root/'population-city-2020.json').read_text(encoding='utf-8'))
 assert set(baseline['values'])=={r['key'] for r in tables['populationCity']['rows']}
 assert sum(v for k,v in baseline['values'].items() if k!='total')==baseline['values']['total']
 d['populationCity2020']=baseline
 (root/'tabulados.js').write_text('window.TABULADOS = '+json.dumps(d,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
 (root/'tabulados-audit.json').write_text(json.dumps({'source':d['source'],'sha256':d['sha256'],'sheets':{k:len(v['rows']) for k,v in tables.items()},'issues':issues},ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'sheets':len(tables),'issues':issues},ensure_ascii=True))
if __name__=='__main__':
 build_data(sys.argv[1])
 from build_dashboard import build
 build()
