# version of our application
CCF_APP_VERSION = '1.0b1'

# tab names of client-detail view
# matches tab numbering in ccf/templates/ccf/client_detail.html
CLIENT_TAB_DETAILS = '0'
CLIENT_TAB_NOTES = '1'
CLIENT_TAB_TREATMENTS = '2'
CLIENT_TAB_MEDICAL = '3'
CLIENT_TAB_CONSULTATION = '4'


def template_symbols(request):
    return {
        'CCF_APP_VERSION': CCF_APP_VERSION,
        'CLIENT_TAB_DETAILS': CLIENT_TAB_DETAILS,
        'CLIENT_TAB_NOTES': CLIENT_TAB_NOTES,
        'CLIENT_TAB_TREATMENTS': CLIENT_TAB_TREATMENTS,
        'CLIENT_TAB_MEDICAL': CLIENT_TAB_MEDICAL,
        'CLIENT_TAB_CONSULTATION': CLIENT_TAB_CONSULTATION,
    }


# number of items per page (for paginators)
CLIENTS_PER_PAGE = 16
NOTES_PER_PAGE = 16
TREATMENTS_PER_PAGE = 16
