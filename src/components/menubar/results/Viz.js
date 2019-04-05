/* Drinkviz
 * 3d modeling of drinks based on ingredients
 */

import React, { Component } from "react";
import * as d3 from "d3";

class Drinkviz extends Component {
  constructor(props) {
    super(props);
    
    // use state to define any variables that may change, 
    // use const for everything else
    this.state = {
      showRecipeCounter: 0
    };
    // you need to bind your functions before declarations
    this.drawPlot = this.drawPlot.bind(this);
    this.highlight = this.highlight.bind(this);
    this.unhighlight = this.unhighlight.bind(this);
  }

  // gets called on first load
  componentDidMount() {
    this.drawPlot();
  }
  
  // gets called whenever state changes, need to define for other variables
  componentDidUpdate() { 
    this.drawPlot();
  }

  drawPlot() {
    const picks = this.props.picks;
    const allDrinks = this.props.allDrinks;
    var drinksSVG = d3.select('#theDrinks');
    
    drinksSVG.append("line")
      .attr("x1",200)
      .attr("x2",725)
      .attr("y1",300)
      .attr("y2",300)
      .attr("stroke","#888")

    drinksSVG.append("line")
      .attr("x1",462)
      .attr("x2",462)
      .attr("y1",45)
      .attr("y2",560)
      .attr("stroke","#888")

    drinksSVG.append("text")
      .text("<- (less)        Sugar        (more) ->")
      .attr ("x",462)
      .attr ("y",615)
      .attr ("text-anchor", "middle")
      .attr ("alignment-baseline", "ideographic")
      .style ("fill","#444")
      .style ("font-size","13pt")
      .attr ("opacity", 0.4)
        
    drinksSVG.append("text")
      .text("<- (less)        Alcohol        (more) ->")
      .attr ("x",875)
      .attr ("y",310)
      .attr ("text-anchor", "middle")
      .attr ("alignment-baseline", "ideographic")
      .style ("fill","#444")
      .style ("font-size","13pt")
      .attr ("opacity", 0.4)
      .attr('transform', 'rotate(270 875 295)')

    drinksSVG.selectAll("circle").remove()
    
    // eslint-disable-next-line
    var abvCirc = drinksSVG.selectAll("#abvCircle")
      .data(allDrinks.Drinks)
      .enter().append("circle")
      .attr("id", "abvCircle")
      .attr ("stroke-width", function(d) {
              if (picks.includes(d.Name)) {
                  return 0.75
              } else {
                  return 0.2
              }
          })
      .attr ("stroke", '#999')
      .attr ("fill-opacity", function(d) {
              if (picks.includes(d.Name)) {
                  return 0.8
              } else {
                  return 0.1
              }
          })
      .attr ("cx",function(d) { 
          // TEMPORARY!!!!! trying to debug getting the spacing right
          if (Math.max(30, (d.Data.Sweetness * 4000) - 25) < 100) {
            //console.log("TOO LOW: " + d.Name + " :: " + d.Data.Sweetness + " :: " + Math.max(30, (d.Data.Sweetness * 4000) - 25));
          }
          if (Math.max(30, (d.Data.Sweetness * 4000) - 25) > 800) {
            //console.log("TOO HIGH: " + d.Name + " :: " + d.Data.Sweetness + " :: " + Math.max(30, (d.Data.Sweetness * 4000) - 25));
          }
          // TEMPORARY!!! ^ trying to debug getting the spacing right
          return Math.min(Math.max(30, (d.Data.Sweetness * 1600) - 25), 825);
      })
      .attr ("cy",function(d) { 
          return Math.min(Math.max(30, (630 - (d.Data.AlcoholUnits * 400))), 570);
      })
      .attr ("r",function(d) { return (d.Data.Volume * Math.min(d.Data.Volume, 3)) + 3; })
      .attr("fill",function(d) { 
              if (d.Data.Style.includes("stirred")) {
                  return "#a5693d";
              } else if (d.Data.Style.includes("bubbly")) {
                  return "#fcf5bf";
              } else if (d.Data.Style.includes("shaken")) {
                  return "#100656";
                  //return "#240ccc";
              } else if (d.Data.Style.includes("fizz")) {
                  return "#f4e381";
              } else if (d.Data.Style.includes("swizzle")) {
                  return "#f27552";
              }    else if (d.Data.Style.includes("built")) {
                  return "#b5390c";
              } else {
                  return "#bbb";
              }
      
      })
    //.on("mouseover", this.highlight())
    //.on("mouseout", this.unhighlight())
  }        
  
  // the tooltip functions
  highlight(d,i) {
    // eslint-disable-next-line
    var circle = d3.select(this)
      .attr("fill-opacity",1)
      .attr("stroke-width",1.5);
    
    d3.select("#tooltip")
        .style("left", d3.event.pageX + 5 + "px")
        .style("top", d3.event.pageY - 30 + "px")
        //.text(d.Name)
        .style("visibility","visible");
    
    d3.select("#drinkName").text(d.Name);
    d3.select("#drinkStyle").text(d.Data.Style);
    d3.select("#drinkIngredients").text(d.Data.IngredientString);
  }

  unhighlight(d,i) {
    // eslint-disable-next-line
    var circle = d3.select(this)
      .attr("fill-opacity", function(d) {
        if (this.state.picks.includes(d.Name)) {
          return 0.95
        } else {
          return 0.05
        }
      })
      .attr ("stroke-width", function(d) {
        if (this.state.picks.includes(d.Name)) {
          return 0.75
        } else {
          return 0.2
        }
      });
    d3.select("#tooltip")
      .style("visibility","hidden");
  }

  render() {
    return (
      <div> 
        <h3 id="viz">Drinks</h3>
        <div className='thePlot'>
          <svg 
            className="bigPlot" 
            id="theDrinks" 
            width="925" 
            height="630">
          </svg>
        </div>
        <div id="tooltip" className="tooltip">
          <span id="drinkName"></span><br />  
          <span id="drinkStyle"></span> 
          <span id="drinkIngredients"></span>
        </div>
        <div id="recipeBox">
          <p id="recipeTitle">Click on a drink to see the recipe</p>
          <p id="recipeIng"></p>
          <p id="recipeBody"></p>
        </div>
      </div>
    );
  }
}

export default Drinkviz;