import React from 'react';
import {GridList, GridTile} from 'material-ui/GridList';
import IconButton from 'material-ui/IconButton';
import StarBorder from 'material-ui/svg-icons/toggle/star-border';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import getMuiTheme from 'material-ui/styles/getMuiTheme'

const lightMuiTheme = getMuiTheme(lightBaseTheme);
const styles = {
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
  },
  gridList: {
    display: 'flex',
    flexWrap: 'nowrap',
    overflowX: 'auto',
  },
  titleStyle: {
    color: 'rgb(0, 188, 212)',
  },
};

const tilesData = [
  {
    img: 'http://test.com:8000/static/myhome/images/req.jpg',
    title: 'Breakfast',
    author: 'jill111',
  },
  {
    img: 'http://test.com:8000/static/myhome/images/3.png',
    title: 'Tasty burger',
    author: 'pashminu',
  },
  {
    img: 'http://test.com:8000/static/myhome/images/4.jpg',
    title: 'Camera',
    author: 'Danson67',
  },
];


class ProductListHorijontalSlider extends React.Component {

  constructor() {
      super();
  }

  render(){
    return (
      <MuiThemeProvider muiTheme={lightMuiTheme}>
      <div style={styles.root}>
        <GridList style={styles.gridList} cols={2.2}>
          {tilesData.map((tile) => (
            <GridTile
              key={tile.img}
              title={tile.title}
              actionIcon={<IconButton><StarBorder color="rgb(0, 188, 212)" /></IconButton>}
              titleStyle={styles.titleStyle}
              titleBackground="linear-gradient(to top, rgba(0,0,0,0.7) 0%,rgba(0,0,0,0.3) 70%,rgba(0,0,0,0) 100%)"
            >
              <img src={tile.img} />
            </GridTile>
          ))}
        </GridList>
      </div>
      </MuiThemeProvider>
    )
  }
}

export default ProductListHorijontalSlider;