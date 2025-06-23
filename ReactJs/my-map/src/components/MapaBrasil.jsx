import { useState, useEffect } from 'react';
import { ComposableMap, Geographies, Geography } from "react-simple-maps";
import { Tooltip } from 'react-tooltip';

const geoUrl = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson";

const estadosBrasileiros = [
  'Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará', 
  'Distrito Federal', 'Espírito Santo', 'Goiás', 'Maranhão', 
  'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Pará', 
  'Paraíba', 'Paraná', 'Pernambuco', 'Piauí', 'Rio de Janeiro', 
  'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 'Roraima', 
  'Santa Catarina', 'São Paulo', 'Sergipe', 'Tocantins'
];


const getColorBasedOnMatriculas = (matriculas, maxMatriculas) => {
  if (!matriculas) return '#3A3A3A';
  
  const ratio = matriculas / maxMatriculas;
  
  
  if (ratio > 0.8) return '#1B5E20';
  if (ratio > 0.6) return '#2E7D32';
  if (ratio > 0.4) return '#388E3C';
  if (ratio > 0.2) return '#43A047';
  return '#81C784';
};

const MapaBrasil = () => {
  const [hoveredState, setHoveredState] = useState(null);
  const [selectedYear, setSelectedYear] = useState('2023');
  const [selectedState, setSelectedState] = useState('Todos');
  const [matriculasData, setMatriculasData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [maxMatriculas, setMaxMatriculas] = useState(0);


  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await fetch(
          `http://localhost:5000/censoescolar?ano=${selectedYear}${selectedState !== 'Todos' ? `&estado=${selectedState}` : ''}`
        );
        const data = await response.json();
        setMatriculasData(data);
        
        if (data.length > 0) {
          const max = Math.max(...data.map(item => item.total_matriculas || 0));
          setMaxMatriculas(max);
        }
      } catch (error) {
        console.error('Erro ao buscar dados:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [selectedYear, selectedState]);

 
  const getMatriculasForState = (stateName) => {
    const estadoData = matriculasData.find(item => item.estado === stateName);
    return estadoData ? {
      total: estadoData.total_matriculas.toLocaleString('pt-BR'),
      value: estadoData.total_matriculas
    } : { total: 'N/D', value: 0 };
  };

  
  const getStateColor = (stateName) => {
    const { value } = getMatriculasForState(stateName);
    
    if (selectedState && selectedState !== stateName && selectedState !== 'Todos') {
      return '#3A3A3A';
    }
    
    return getColorBasedOnMatriculas(value, maxMatriculas);
  };

  return (
    <div style={{ 
      width: "100%", 
      maxWidth: "900px", 
      margin: "2rem auto",
      padding: "1.5rem",
      borderRadius: "12px",
      boxShadow: "0 8px 30px rgba(0,0,0,0.3)",
      backgroundColor: "#1E1E1E",
      transition: "all 300ms ease",
      color: "#EEE"
    }}>
      <h2 style={{ 
        textAlign: "center", 
        color: "#FFF",
        marginBottom: "1.5rem",
        fontSize: "1.8rem",
        fontWeight: "600",
        textShadow: "0 2px 4px rgba(0,0,0,0.3)"
      }}>Censo Escolar do Brasil</h2>
      
    
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        gap: '20px',
        marginBottom: '1.5rem',
        flexWrap: 'wrap'
      }}>
        <div>
          <label htmlFor="year-select" style={{
            display: 'block',
            marginBottom: '0.5rem',
            fontWeight: '500',
            color: '#CCC'
          }}>Ano:</label>
          <select
            id="year-select"
            value={selectedYear}
            onChange={(e) => setSelectedYear(e.target.value)}
            style={{
              padding: '0.5rem 1rem',
              borderRadius: '6px',
              border: '1px solid #444',
              backgroundColor: '#2D2D2D',
              color: '#EEE',
              cursor: 'pointer',
              minWidth: '120px'
            }}
          >
            <option value="2023">2023</option>
            <option value="2024">2024</option>
          </select>
        </div>
        
        <div>
          <label htmlFor="state-select" style={{
            display: 'block',
            marginBottom: '0.5rem',
            fontWeight: '500',
            color: '#CCC'
          }}>Estado:</label>
          <select
            id="state-select"
            value={selectedState}
            onChange={(e) => setSelectedState(e.target.value)}
            style={{
              padding: '0.5rem 1rem',
              borderRadius: '6px',
              border: '1px solid #444',
              backgroundColor: '#2D2D2D',
              color: '#EEE',
              cursor: 'pointer',
              minWidth: '200px'
            }}
          >
            <option value="Todos">Todos os Estados</option>
            {estadosBrasileiros.map(state => (
              <option key={state} value={state}>{state}</option>
            ))}
          </select>
        </div>
      </div>

      {loading && (
        <div style={{
          textAlign: 'center',
          margin: '1rem 0',
          color: '#4FC3F7',
          fontWeight: '500'
        }}>
          Carregando dados...
        </div>
      )}

      <ComposableMap
        projection="geoMercator"
        projectionConfig={{
          scale: 700,
          center: [-54, -15]
        }}
        width={900}
        height={650}
        style={{
          borderRadius: "8px",
          overflow: "hidden",
          backgroundColor: "#2D2D2D",
          boxShadow: "0 4px 12px rgba(0,0,0,0.2)"
        }}
      >
        <Geographies geography={geoUrl}>
          {({ geographies }) =>
            geographies.map((geo) => {
              const stateName = geo.properties.name;
              const matriculas = getMatriculasForState(stateName);
              
              return (
                <Geography
                  key={geo.rsmKey}
                  geography={geo}
                  fill={getStateColor(stateName)}
                  stroke={selectedState === stateName ? "#FFF" : "#555"}
                  strokeWidth={selectedState === stateName || selectedState === 'Todos' ? 1.2 : 0.7}
                  data-tooltip-id="state-tooltip"
                  data-tooltip-content={`${stateName} (${selectedYear}) - Matrículas: ${matriculas.total}`}
                  onMouseEnter={() => {
                    setHoveredState(stateName);
                  }}
                  onMouseLeave={() => {
                    setHoveredState(null);
                  }}
                  style={{
                    default: { outline: "none" },
                    hover: { 
                      fill: '#FF7043',
                      outline: "none",
                      stroke: "#FFF",
                      strokeWidth: 1.8,
                      filter: "drop-shadow(0 0 10px rgba(255,112,67,0.6))",
                      transition: "all 250ms ease",
                      transform: "translateY(-3px)"
                    },
                    pressed: { 
                      fill: '#E64A19',
                      outline: "none",
                      transform: "scale(0.98)"
                    },
                  }}
                />
              );
            })
          }
        </Geographies>
      </ComposableMap>

      <Tooltip 
        id="state-tooltip" 
        place="top"
        style={{
          backgroundColor: "#424242",
          color: "#FFF",
          borderRadius: "6px",
          padding: "8px 16px",
          fontSize: "14px",
          fontWeight: "500",
          boxShadow: "0 4px 20px rgba(0,0,0,0.3)",
          zIndex: 1000,
          border: "1px solid #555"
        }}
      />

 
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        marginTop: '1rem',
        alignItems: 'center',
        gap: '1rem',
        flexWrap: 'wrap'
      }}>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <div style={{
            width: '20px',
            height: '20px',
            backgroundColor: '#81C784',
            marginRight: '0.5rem',
            border: '1px solid #555'
          }}></div>
          <span>Menos matrículas</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <div style={{
            width: '20px',
            height: '20px',
            backgroundColor: '#1B5E20',
            marginRight: '0.5rem',
            border: '1px solid #555'
          }}></div>
          <span>Mais matrículas</span>
        </div>
      </div>

      {hoveredState && (
        <div style={{
          position: "absolute",
          bottom: "20px",
          left: "50%",
          transform: "translateX(-50%)",
          backgroundColor: "rgba(255,255,255,0.9)",
          color: "#333",
          padding: "8px 16px",
          borderRadius: "20px",
          fontSize: "14px",
          fontWeight: "600",
          transition: "all 300ms ease",
          opacity: hoveredState ? 1 : 0,
          boxShadow: "0 4px 12px rgba(0,0,0,0.2)"
        }}>
          {hoveredState} - {selectedYear}: {getMatriculasForState(hoveredState).total} matrículas
        </div>
      )}
    </div>
  );
};

export default MapaBrasil;