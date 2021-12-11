import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Redirect } from 'react-router-dom';
import { VictoryBar } from 'victory';
import { VictoryChart } from 'victory';
import { VictoryAxis } from 'victory';

function User({ user, logout })
{
    //Display user info
    //get the id of the champion
    const [regions, setRegions] = useState(
        {
            'Bandle City': 0,
            'Bilgewater': 0,
            'Demacia': 0,
            'Ionia': 0,
            'Ixtal': 0,
            'Noxus': 0,
            'Piltover': 0,
            'Shadow Isles': 0,
            'Shurima': 0,
            'Targon': 0,
            'Freljord': 0,
            'The Void': 0,
            'Zaun': 0,
            'Runeterra': 0
        });

    if (user.userID === '-1') {
        return <Redirect to='/' />
    }

    for (let i = 0; i < user.favouriteDetail.length; i += 1) {
        for (var key in regions) {
            if (user.favouriteDetail[i].Region === key) {
                regions[key] += 1
                break
            }
        }
    }


    console.log(regions['Runeterra'])
    return (
        <div className='users'>
            <h1 className='title'>Welcome {user.name}</h1>
            <br />
            <h1 className='intro'>
                Your Favorite Champions
            </h1>
            {/* Image & Name */}
            {
                user.favouriteDetail.map((item) => (
                    <div className='item'>
                        <Link to={`/champion/${item.Champion_ID}`}>
                            <div><img src={item.Image_Url} alt='' /></div>
                        </Link>
                        {/* <div className='champion-label'><a href={item.Main_Page_Url}>{item.Name}</a></div> */}
                        <div className='champion-label'>
                            <Link to={`/champion/${item.Champion_ID}`}>
                                <div>{item.Name}</div>
                            </Link>
                        </ div>
                    </div>
                ))}
            <div className='graphs'>
                <h1> Region Preference </ h1>
                {/* Region Bar Chart */}
                <div >
                    <VictoryChart
                        domainPadding={0}
                        style={{
                            label: { fontSize: 15 }
                        }}
                    >
                        <VictoryBar
                            data={[
                                { x: "Bandle City", y: regions['Bandle City'] },
                                { x: 'Bilgewater', y: regions['Bilgewater'] },
                                { x: 'Demacia', y: regions['Demacia'] },
                                { x: 'Ionia', y: regions['Ionia'] },
                                { x: 'Ixtal', y: regions['Ixtal'] },
                                { x: 'Noxus', y: regions['Noxus'] },
                                { x: 'Piltover', y: regions['Piltover'] },
                                { x: 'Shadow Isles', y: regions['Shadow Isles'] },
                                { x: 'Shurima', y: regions['Shurima'] },
                                { x: 'Targon', y: regions['Targon'] },
                                { x: 'Freljord', y: regions['Freljord'] },
                                { x: 'The Void', y: regions['The Void'] },
                                { x: 'Zaun', y: regions['Zaun'] },
                                { x: 'Runeterra', y: regions['Runeterra'] }
                            ]}
                            barWidth={5}
                            style={{
                                data: {
                                    fill: "#c43a31", stroke: "black", strokeWidth: 1
                                },
                            }}
                            animate={{
                                onExit: {
                                    duration: 500,
                                    before: () => ({
                                        _y: 0,
                                        fill: "orange",
                                        label: "BYE"
                                    })
                                }
                            }}
                        />
                        <VictoryAxis
                            style={{
                                tickLabels: { fontSize: 5, padding: 0 }
                            }}
                        />
                    </ VictoryChart>

                </ div>
            </div>
            {/* Logout Button */}
            < button onClick={logout} className='logoutButton'> Logout</button>
        </div >
    )
}

export default User;