-> [/login] show login (if not already logged in) 
	actions:
	-> user id/pwd and submit
-> [/subs] show list of subscriptions (paging) (left Navigation: new/remove subscription),(right nav: logout)
    show categories in combo and on selection render subscriptions as list (table)
	actions:
	-> click on link: navigate to item list page
-> [/subsitem] show list of rss items (paging) (left Navigation: back to rss list),(right nav: logout)
	in header, show breadcrumb with "title"
	actions:
	-> click on link: navigate shows contents of the rss item
-> [/subsitemcontent] show content of rss item, (left navigation: back to item list),(right nav: logout)
	in header, show breadcrumb with "title-> item title"
	in footer, show "previous" and "next" link 
    actions:
	-> 