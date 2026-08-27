{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "0c6fada3-9641-4ffa-83fe-8892be09c7b3",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "8af6809f-5735-4711-8dc8-733c19cc31f4",
   "metadata": {},
   "outputs": [],
   "source": [
    "df = pd.read_csv('data/phishing_email.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "ce8017de-294c-4bce-a40e-b5d353b2f445",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>text_combined</th>\n",
       "      <th>label</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>hpl nom may 25 2001 see attached file hplno 52...</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>nom actual vols 24 th forwarded sabrae zajac h...</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>enron actuals march 30 april 1 201 estimated a...</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>hpl nom may 30 2001 see attached file hplno 53...</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>hpl nom june 1 2001 see attached file hplno 60...</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>82481</th>\n",
       "      <td>info advantageapartmentscom infoadvantageapart...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>82482</th>\n",
       "      <td>monkeyorg helpdeskmonkeyorg monkeyorg hi josep...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>82483</th>\n",
       "      <td>help center infohelpcentercoza_infohelpcenterc...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>82484</th>\n",
       "      <td>metamask infosofamekarcom verify metamask wall...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>82485</th>\n",
       "      <td>fastway infofastwaycoza_infofastwaycoza_infofa...</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>82486 rows × 2 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "                                           text_combined  label\n",
       "0      hpl nom may 25 2001 see attached file hplno 52...      0\n",
       "1      nom actual vols 24 th forwarded sabrae zajac h...      0\n",
       "2      enron actuals march 30 april 1 201 estimated a...      0\n",
       "3      hpl nom may 30 2001 see attached file hplno 53...      0\n",
       "4      hpl nom june 1 2001 see attached file hplno 60...      0\n",
       "...                                                  ...    ...\n",
       "82481  info advantageapartmentscom infoadvantageapart...      1\n",
       "82482  monkeyorg helpdeskmonkeyorg monkeyorg hi josep...      1\n",
       "82483  help center infohelpcentercoza_infohelpcenterc...      1\n",
       "82484  metamask infosofamekarcom verify metamask wall...      1\n",
       "82485  fastway infofastwaycoza_infofastwaycoza_infofa...      1\n",
       "\n",
       "[82486 rows x 2 columns]"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "21c15a9d-8a88-48f9-851f-be10c57d2fb2",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Index(['text_combined', 'label'], dtype='object')"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.columns"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "e5d1f552-6a04-4bc0-9bf3-e75d3f8b9f05",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(82486, 2)"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "dc21859d-80cf-4de3-a060-48df85970a76",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<bound method NDFrame.head of                                            text_combined  label\n",
       "0      hpl nom may 25 2001 see attached file hplno 52...      0\n",
       "1      nom actual vols 24 th forwarded sabrae zajac h...      0\n",
       "2      enron actuals march 30 april 1 201 estimated a...      0\n",
       "3      hpl nom may 30 2001 see attached file hplno 53...      0\n",
       "4      hpl nom june 1 2001 see attached file hplno 60...      0\n",
       "...                                                  ...    ...\n",
       "82481  info advantageapartmentscom infoadvantageapart...      1\n",
       "82482  monkeyorg helpdeskmonkeyorg monkeyorg hi josep...      1\n",
       "82483  help center infohelpcentercoza_infohelpcenterc...      1\n",
       "82484  metamask infosofamekarcom verify metamask wall...      1\n",
       "82485  fastway infofastwaycoza_infofastwaycoza_infofa...      1\n",
       "\n",
       "[82486 rows x 2 columns]>"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.head"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ee19c194-56d9-432c-b46a-fdb3916abe0f",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
