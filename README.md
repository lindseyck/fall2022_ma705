# MA705 Final Project

This repository contains files used in the MA705 dashboard project.

The final dashboard is deployed on Heroku [here](https://fall2022_ma705.herokuapp.com).

## Dashboard Description
This dashboard allows a user to search for artist name, painting title, or keywords within to find paintings currently on display at three Boston area museums: Harvard Art Museum, the Isabella Stewart Gardener Museum, and the Museum of Fine Arts Boston. The top artists represented at these museums are graphically displayed to give users an idea of what they can expect to see at these museums, and to offer suggestions of artists to look into. The chart below contains all of the artists, painting titles, museum where the work is located, and a URL to view details of the artwork.

### Data Sources

The Harvard Art Museum data were gathered using their REST API and filtering down to Classification = 'Paintings'. After cleaning the artist names and excluding any unknown, the final dataframe contained: Object ID, Artist, Title, URL, Artist Gender, Division, Medium, Colors, Dated, Century, Culture, and Description. Ultimately, only Object ID, Artist, Title, and URL were used as the remaining variables were unavailable in the additional data sources

Data were gather from the Isabella Stewart Gardner museum using web scraping. Each piece in the museum has a unique ID number and a webpage displaying the object details. Exploring the website showed that object IDs seem to range between 10000 and 16000. URLs were tested with each object ID and invalid addresses were excluded. Any webpages including the word "paint" were included in the dataset, and any including the word "stolen" were excluded as these will not be viewable.  

MFA data were gather by scraping their collection websites that contained paintings currently on view. At present, there are only 28 paintings that fit these criteria. It's possible that the collection on the website is incomplete, but the project is limited to the data available.

- https://harvardartmuseums.org/collections?worktype%5B%5D=painting
- https://www.gardnermuseum.org/experience/collection
- https://collections.mfa.org/collections/314108/american-paintings/objects?filter=onview%3Atrue#filters
- https://collections.mfa.org/collections/314107/european-paintings/objects?filter=onview%3Atrue#filters
- https://dash.plotly.com/
- https://github.com/plotly/dash-table/issues/370
- https://github.com/plotly/dash-table/issues/222

