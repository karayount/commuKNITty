# Overview

CommuKNITty is a full-stack web application where knitters can plan their yarny adventures. Knitters can see their current yarn inventory in their Basket, and maintain preferences of what they like to knit. From those preferences, users receive personalized recommendations of things to knit through calls to the Ravelry API. CommuKNITty maintains a Postgres database of knitting patterns and queries it to provide recommendations of what to knit with a yarn in a user's Basket. Knitters can search for instructions for specific items, like a scarf or beanie, and view local yarn shops, retrieved from the Yelp API and displayed with Google Maps. If solo knitting gets lonely, they can join the larger commuKNITty and find a weekly knit night nearby.

# Technologies

- Postgres
- SQLAlchemy
- Python
- Flask
- Jinja
- Javascript
- jQuery
- HTML
- CSS
- Bootstrap
- APIs: Ravelry, Yelp, Google Maps
- Testing with unittest and Selenium WebDriver


# CommuKNITty
 
![Landing Page](/docs/screen-shot-login-confirm.png?raw=true)


### Profile

User profile displays user's personal data (including lifetime miles knit), and current preferences, which are retrieved by database query, and displayed with Jinja templating.

![User Profile Page](/docs/screen-shot-profile.png?raw=true)

Users can update their preferences by opening the form below. When a preference box is checked or unchecked, an AJAX request is sent to the server, which updates the database record, On return, the user's new preference is reflected in the display. 

![Update Preferences](/docs/screen-shot-profile-update-form.png?raw=true)


### Basket

The basket features stores a user's personal yarn inventory. Each yarn displays a stock photo for that yarn company's yarn line (similar to make and model for cars) along with color and yardage for the yarn in this basket. 

![Basket](/docs/screen-shot-basket.png?raw=true)

Each displayed yarn has a link to see patterns, which are suggestions of what to make with the yarn. The patterns are returned from a database query of patterns for which there is a project that was created using the pattern with the input yarn.

![What to Make with Yarn](/docs/screen-shot-yarn-based-search-results.png?raw=true)

Users can also add new yarns to their basket, by clicking the Add yarn to your basket button. A form displays in a modal window asking for a search term, which is used to query the database against the yarn name field in the yarns table. 

![Find Yarn to Add](/docs/screen-shot-basket-search-yarn.png?raw=true)

Results are displayed by replacing the modal window content with a new form to add the yarn. The user can choose a matching yarn from the drop down, and add yardage and color for this yarn. On submit, the basket page displays the new yarn.

![Add Yarn](/docs/screen-shot-basket-add-yarn.png?raw=true)


### Find Patterns

To help knitters plan their next project, personalized recommendations are provided. The user's preferences are added to the url for a request sent to the Ravelry API. The first 5 matches are displayed, but the See More button allows users to view the full list. 

![Find Patterns](/docs/screen-shot-find-patterns-landing.png?raw=true)

![See More](/docs/screen-shot-find-patterns-see-more.png?raw=true, "See More")

If a user wants to knit a particular type of item, like a beanie or a cardigan, the selection form is accessed by the "Looking for something specific?" button. Submitting this form requests the same pattern set from the Ravelry API as the personalized recommendations, but uses input paramaters, rather than user's preferences.

![Custom Search Form](/docs/screen-shot-find-patterns-search-form.png?raw=true)

![Custom Search](/docs/screen-shot-find-patterns-search-results.png?raw=true)


### Nearby

Knitters can find local yarn shops, which were sourced though the Yelp API searching for category "knitting supplies." These shops are plotted on a Google Maps map, and clicking a marker displays an info window with a link to the Yelp page for the shop.
Local weekly knit nights are listed, so users can engage with their local maker community.

![Custom Search](/docs/screen-shot-local.png?raw=true)


### About the author

Kara Yount is a software engineer with technical consulting experience. She graduated from [Hackbright](https://hackbrightacademy.com/) in Winter 2016, and lives in San Francisco. Find Kara on [LinkedIn](https://www.linkedin.com/in/karayount)


