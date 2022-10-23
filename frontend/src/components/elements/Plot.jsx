import React, { useEffect, useRef, useState }  from 'react';
import '../styles/elements/plot.scss';
import Plot from 'react-plotly.js';

const MyPlot = (props) => {
    const plotWidth = (windowWidth, n = 2, widthList = [1200]) => {
        if (widthList.length !== n - 1) {
            throw(Error('plotWidth: properties error'));
        }
        for (let i = n ; i > 1; i--) {
            if (windowWidth > widthList[n-2]) {
                return((windowWidth - (i + 1) * 50) / i);
            }
            return(windowWidth - 100);
        }
    }

    const ref = useRef(null);
    const [ width, setWidth ] = useState(plotWidth(window.innerWidth))

    const resizeListener = () => {
        setWidth(plotWidth(window.innerWidth));
    };

    useEffect(() => {
        window.addEventListener('resize', resizeListener);
    }, []);

    return (
        <div ref={ref} className={"plot " + props.className}
             style={{width: `${width}px`}}>
            <Plot
                data={[props.data]}
                layout={{
                    paper_bgcolor: '#1f356e',
                    plot_bgcolor: 'rgba(0, 0, 0, 0.2)',
                    width: width,
                    height: 500,
                    xaxis: {
                        autorange: props.xAutorange,
                        color: '#eae9c1',
                        title: props.xTitle
                    },
                    yaxis: {
                        autorange: props.yAutorange,
                        color: '#eae9c1',
                        title: props.yTitle
                    },
                    margin: {
                        l: 40,
                        r: 40,
                        t: 40,
                        b: 40
                    },
                    title: {
                        text: props.title,
                        font: {
                            color: '#eae9c1'
                        }
                    }
                }}
            />
            <div className={'input-gp'}>
                <label for={'Xaxis'} className={'input-label'}>
                    X
                </label>
                <select id='Xaxis' className={'input'}>
                    <option>Пункт 1</option>
                    <option>Пункт 2</option>
                </select>
                <label htmlFor={'Yaxis'} className={'input-label'}>
                    Y
                </label>
                <select id='Yaxis' className={'input'}>
                    <option>Пункт 1</option>
                    <option>Пункт 2</option>
                </select>
            </div>
        </div>
    )
}

export default MyPlot;